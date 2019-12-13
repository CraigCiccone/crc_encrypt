"""Functions related to encryption."""

import os
from zipfile import ZipFile, ZIP_DEFLATED

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


from config import (
    DB_FILE_PATH,
    FILE_CRYPT,
    FILE_KEY,
    FILE_PRIV,
    FILE_PUB,
    FILE_UNENCRYPTED,
    TMP_DIR,
)
from db import Archive, KeyPair
from encryption.keys import (
    generate_symmetric_key,
    load_public_key,
    write_key_pair,
)
from utils.archive import zip_dir, zip_files
from utils.helpers import Result


def db_backup_wrapper(dst, key_pair_name):
    """Wrapper function used as the main entry point to backup the database.

    Args:
        dst (str): The path where the DB backup will be stored.
        key_pair_name (str): Key pair that will be used to secure the backup.
    """
    msg = ""
    source = DB_FILE_PATH
    destination = os.path.abspath(dst)
    key_pair = KeyPair.get(KeyPair.name == key_pair_name)

    # Ensure the destination is a directory
    if not os.path.isdir(dst):
        msg = "The destination must be a directory"
        print(msg)
        return Result(False, msg)

    # Verify that the key pair has a password
    if not key_pair.password:
        msg = "A password protected key pair must be used for database backups"
        print(msg)
        return Result(False, msg)
    elif not key_pair.password.strong:
        msg = "Using a key pair with a weak password"
        print(msg)

    encrypt_wrapper(source, destination, key_pair_name)

    tmp_path = os.path.abspath(os.path.join(destination, TMP_DIR))
    write_key_pair(key_pair_name, tmp_path)

    # Add the key pair to the DB backup bundle
    archive_path = os.path.join(destination, f"{os.path.basename(source)}.zip")
    priv_path = os.path.join(tmp_path, f"{key_pair_name}{FILE_PRIV}")
    pub_path = os.path.join(tmp_path, f"{key_pair_name}{FILE_PUB}")
    with ZipFile(archive_path, "a", ZIP_DEFLATED, compresslevel=9) as zip_file:
        zip_file.write(priv_path, os.path.basename(priv_path))
        zip_file.write(pub_path, os.path.basename(pub_path))

    return Result(True, msg)


def encrypt_archive(name, archive, destination, symmetric_key):
    """Encrypts a zip archive using a symmetric key.

    Args:
        name (str): The name of the encrypted archive to be created.
        archive (str): Path to the zip file to be encrypted.
        destination (str): Where to store the encrypted archive.
        symmetric_key (bytes): The symmetric key used to encrypt the archive.

    Returns:
        str: The path to the encrypted output archive.
    """
    output_file = os.path.join(destination, name)
    with open(archive, "rb") as source_file:
        archive_bytes = source_file.read()

    # Encrypt the archive
    encrypted_archive_bytes = Fernet(symmetric_key).encrypt(archive_bytes)

    # Store the encrypted archive
    with open(output_file, "xb") as dest_file:
        dest_file.write(encrypted_archive_bytes)

    return output_file


def encrypt_symmetric_key(name, public_key_bytes, destination, symmetric_key):
    """Encrypts a symmetric key using an asymmetric public key.

    Args:
        name (str): The name of the symmetric key.
        public_key_bytes (bytes): Public key used to encrypt the symmetric key.
        destination (str): Where the encrypted symmetric key will be stored.
        symmetric_key (bytes): The symmetric key to be encrypted.

    Returns:
        bytes: The encrypted symmetric key.
    """
    public_key = load_public_key(public_key_bytes)

    # Encrypt the symmetric key using the public key
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None,
        ),
    )

    # Store the encrypted symmetric key at the desired location
    key_file = os.path.join(destination, name)
    with open(key_file, "xb") as dest_file:
        dest_file.write(encrypted_symmetric_key)

    return encrypted_symmetric_key


def encrypt_wrapper(source, dst, key_pair_name):
    """Wrapper function used as the main entry point to encrypt an archive.

    Args:
        source (str): Path to the file or directory that will be encrypted.
        dst (str): Path where the encrypted archive will be stored.
        key_pair_name (str): The name of the key pair used for the encryption.
    """
    key_pair = KeyPair.get(KeyPair.name == key_pair_name)

    # Ensure if the source is a file or dir. Ensure the destination is a dir
    if os.path.isdir(source):
        is_dir = True
    elif os.path.isfile(source):
        is_dir = False
    else:
        print("Source is invalid")
        return Result(False, "Source is invalid")

    if not os.path.isdir(dst):
        msg = "The destination must be a directory"
        print(msg)
        return Result(False, msg)

    # Get fully qualified paths for source and destination
    source = os.path.abspath(source)
    destination = os.path.abspath(dst)

    # Set the names of the archives and symmetric key based on the source
    name = f"{os.path.basename(source)}"
    name_unencrypted = f"{name}{FILE_UNENCRYPTED}"
    name_encrypted = f"{name}{FILE_CRYPT}"
    sym_key_name = f"{name}{FILE_KEY}"

    tmp_dir = os.path.join(destination, TMP_DIR)
    os.mkdir(tmp_dir)

    if is_dir:
        zip_dir(name_unencrypted, source, tmp_dir)
    else:
        zip_files(name_unencrypted, [source], tmp_dir)

    sym_key_bytes = generate_symmetric_key()

    # Encrypt the archive using the symmetric key
    archive = os.path.join(tmp_dir, name_unencrypted)
    encrypt_archive(name_encrypted, archive, tmp_dir, sym_key_bytes)

    # Encrypt the symmetric key using the asymmetric key pair
    encrypt_symmetric_key(
        sym_key_name, key_pair.public_key, tmp_dir, sym_key_bytes
    )

    # Zip the encrypted archive and the symmetric key into one zip bundle
    sym_key_path = os.path.join(tmp_dir, sym_key_name)
    encrypted_arch_path = os.path.join(tmp_dir, name_encrypted)
    zip_files(f"{name}.zip", [encrypted_arch_path, sym_key_path], destination)

    Archive.create(
        name=name, src_path=source, dst_path=destination, key_pair=key_pair
    )

    return Result(True, "")
