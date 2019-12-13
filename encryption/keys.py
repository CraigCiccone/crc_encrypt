"""Functions related to symmetric and asymmetric cryptographic keys."""

import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from peewee import IntegrityError

from db import KeyPair, Password
from utils.helpers import Result
from utils.validation import strong_password


def generate_asymmetric_key_pair(name, hint="", pw=None):
    """Generates an asymmetric key pair.

    The private key can optionally be protected with a password. The keys are
    RSA format using a key size of 4096 with PEM encoding.

    Args:
        name (str): Used to uniquely name the keys.
        hint (Optional[str]): Information to help remember a password.
        pw (Optional[str]): The password used to encrypt the private key.

    Returns:
        Result: Details of the function's results.
    """
    password = None
    pw_msg = ""
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096, backend=default_backend()
    )
    public_key = private_key.public_key()

    # Get the private key as bytes. Only encrypt the private key using a
    # password if a password is provided.
    if pw:
        # Validate the password
        result = strong_password(pw)
        pw_msg = result.msg
        if not result.success:
            return result

        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                pw.encode("utf-8")
            ),
        )
        password = Password(
            hint=hint, strong=True if result.msg == "" else False,
        )
        password.save()
    else:
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

    # Get the public key as bytes
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Write the key pair to the database. Include the password if provided.
    result = store_key_pair(name, public_bytes, private_bytes, password)
    return Result(
        result.success, f"{pw_msg}\n\n{result.msg}" if pw_msg else result.msg
    )


def generate_symmetric_key():
    """Generates a symmetric key using cryptography's Fernet.

    Returns:
        bytes: The symmetric key.
    """
    return Fernet.generate_key()


def import_key_pair(name, private_path, public_path, hint=None, pw=None):
    """Stores a new key pair in the DB.

    Args:
        name (str): The unique name used to identify the key pair.
        private_path (str): The path to the private key file.
        public_path (str): The path to the public key file.
        hint (Optional[str]): A hint to remember the password.
        pw (Optional[str]): An optional password to secure the private key.
    """

    # Test for existence of the key pair files provided
    if not os.path.isfile(private_path):
        msg = "The private key must be a valid file."
        print(msg)
        return Result(False, msg)
    elif not os.path.isfile(public_path):
        msg = "The public key must be a valid file."
        print(msg)
        return Result(False, msg)

    # Read the private and public key
    with open(private_path, "rb") as private_key_file:
        private_key_bytes = private_key_file.read()
    with open(public_path, "rb") as public_key_file:
        public_key_bytes = public_key_file.read()

    # Set password metadata if a password is provided
    password = None
    if pw:

        # Validate the password
        result = strong_password(pw)
        if not result.success:
            return Result(
                False, "Cannot import key due to password simplicity"
            )

        # Store the password metadata in the DB
        password = Password(
            hint=hint, strong=True if result.msg == "" else False,
        )
        password.save()

    # Ensure that the keys are valid and can be loaded
    load_private_key(private_key_bytes, pw)
    load_public_key(public_key_bytes)

    # Store the key pair
    return store_key_pair(name, public_key_bytes, private_key_bytes, password)


def load_private_key(private_key_bytes, pw=None):
    """Reads a private key in the PEM format from a file.

    Args:
        private_key_bytes (bytes): The private key as bytes.
        pw (Optional[str]): The password used to encrypt the private key.

    Returns:
        A private key object.
    """

    # Convert the password to bytes if it is provided
    if pw:
        pw = pw.encode("utf-8")

    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=pw if pw else None,
        backend=default_backend(),
    )
    return private_key


def load_public_key(public_key_bytes):
    """Loads a public key from bytes.

    Args:
        public_key_bytes (bytes): The public key as bytes.

    Returns:
        A public key object.
    """
    public_key = serialization.load_pem_public_key(
        public_key_bytes, backend=default_backend()
    )
    return public_key


def store_key_pair(name, public_bytes, private_bytes, password=None):
    """Writes the key pair to the database.

    Password metadata is included if a password is provided.

    Args:
        name (str): The unique name for the key pair.
        public_bytes (bytes): The public key as bytes.
        private_bytes (bytes): The private key as bytes.
        password (Optional[Password]): Password used to secure the private key.
    """
    try:
        KeyPair.create(
            name=name,
            public_key=public_bytes,
            private_key=private_bytes,
            password=password if password else None,
        )
    except IntegrityError:
        return Result(False, f'Key Pair with name "{name}" already exists')

    return Result(True, "")


def write_all_key_pairs(destination):
    """Write all key pairs to corresponding files.

    Args:
        destination (str): The location to store the key files.
    """
    key_pairs = KeyPair.select()

    # Ensure the destination is a directory
    if not os.path.isdir(destination):
        msg = "The destination must be a directory"
        print(msg)
        return Result(False, msg)

    # Store each key pair in its own directory
    for key_pair in key_pairs:
        dst = os.path.join(destination, key_pair.name)
        os.mkdir(dst)
        write_key_pair(key_pair.name, dst)

    return Result(True, "")


def write_key_pair(name, destination):
    """Write a key pair to corresponding files.

    Args:
        name (str): The name of the key pair to write to files.
        destination (str): The location to store the key files.
    """
    key_pair = KeyPair.get(KeyPair.name == name)

    # Ensure the destination is a directory
    if not os.path.isdir(destination):
        msg = "The destination must be a directory"
        print(msg)
        return Result(False, msg)

    # Store the key pairs in files
    private_name = f"{key_pair.name}_PRIVATE.key"
    public_name = f"{key_pair.name}_public.key"
    with open(os.path.join(destination, private_name), "xb") as private_key:
        private_key.write(key_pair.private_key)
    with open(os.path.join(destination, public_name), "xb") as public_key:
        public_key.write(key_pair.public_key)

    return Result(True, "")
