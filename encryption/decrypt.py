"""Functions related to decryption."""

import os
from shutil import copyfile
from zipfile import ZipFile

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from peewee import DoesNotExist

from config import DB_FILE, DB_FILE_PATH, DB_PATH, TMP_DIR
from db import KeyPair
from encryption.keys import load_private_key
from utils.archive import extract_files
from utils.helpers import Result


def db_restore_wrapper(source, password):
    """Wrapper function used as the main entry point to decrypt an archive.

    Args:
        source (str): Path to the source file archive that is to be decrypted.
        password (str): The password used to encrypt the symmetric key.
    """
    source_path = os.path.abspath(source)
    source = os.path.basename(source)

    # Backup the original DB file
    count = 1
    backup_file = os.path.join(DB_PATH, f"{DB_FILE}.back_{count}")
    while os.path.exists(backup_file):
        count += 1
        backup_file = os.path.join(DB_PATH, f"{DB_FILE}.back_{count}")
    copyfile(DB_FILE_PATH, backup_file)

    # Extract the DB backup
    tmp_path = os.path.join(DB_PATH, TMP_DIR)
    extract_files(source_path, tmp_path)

    # Inspect the DB backup zip for the private key
    private_path = None

    with ZipFile(source_path, "r") as zip_file:
        files = zip_file.namelist()

    for file in files:
        if "_PRIVATE.key" in file:
            private_path = os.path.join(tmp_path, file)
            break

    # Read the private key and decrypt the backup
    with open(private_path, "rb") as private_key_file:
        private_key_bytes = private_key_file.read()
    decrypt_backup(source, DB_PATH, private_key_bytes, password)

    return Result(True, "")


def decrypt_archive(source, destination, key_pair_name, pw=None):
    """Decrypt an encrypted archive using a private key and a symmetric key.

    First the symmetric key must be decrypted via the private key. Then the
    symmetric key is used to decrypt the encrypted archive.

    Args:
        source (str): Path to the encrypted archive.
        destination (str): Where the decrypted archive will be stored.
        key_pair_name (str): Name of the key pair used to encrypt the archive.
        pw (Optional[str]): The password used to encrypt the private key.
    """

    # Ensure the source and destination are valid
    if not os.path.isdir(destination):
        msg = "The destination must be a directory"
        print(msg)
        return Result(False, msg)
    elif not os.path.isfile(source):
        msg = "The source must be a file"
        print(msg)
        return Result(False, msg)

    # Set the name for the decrypted archive
    base_name = os.path.splitext(os.path.basename(source))[0]
    name = base_name.replace("_ENCRYPTED", "")

    # Get the private key from the key pair provided
    try:
        private_key = KeyPair.get(KeyPair.name == key_pair_name).private_key
    except DoesNotExist:
        msg = f"Key pair does not exist : {key_pair_name}"
        print(msg)
        return Result(False, msg)

    # Create a temporary working directory
    tmp_dir = os.path.join(destination, TMP_DIR)
    os.mkdir(tmp_dir)

    extract_files(source, tmp_dir)

    decrypt_core(destination, private_key, pw, base_name, name)

    return Result(True, "")


def decrypt_backup(source, destination, private_key_bytes, pw):
    """Decrypts a DB backup archive.

    Args:
        source (str): Path to the encrypted DB backup archive.
        destination (str): Where the decrypted backup archive will be stored.
        private_key_bytes (bytes): The private key as bytes.
        pw (str): The password used to encrypt the private key.
    """
    base_name = os.path.splitext(os.path.basename(source))[0]
    name = base_name.replace("_ENCRYPTED", "")

    decrypt_core(destination, private_key_bytes, pw, base_name, name)


def decrypt_core(destination, private_key, pw, base_name, name):
    """The main shared logic used for archive decryption.

    Args:
        destination (str): Where the decrypted archive will be stored.
        private_key (bytes): The private key as bytes.
        pw (str): The password used to encrypt the private key.
        base_name (str): The name of the archive.
        name (str): The name of the archive with temporary tags removed.
    """
    tmp_dir = os.path.join(destination, TMP_DIR)

    # Decrypt the symmetric key
    sym_key_path = os.path.join(tmp_dir, f"{base_name}_KEY.key")
    symmetric_key = decrypt_symmetric_key(private_key, sym_key_path, pw)

    # Read the encrypted archive as bytes
    source_path = os.path.join(tmp_dir, f"{base_name}_ENCRYPTED.zip")
    with open(source_path, "rb") as src_file:
        encrypted_archive_bytes = src_file.read()

    # Decrypt the archive using the symmetric key
    archive_bytes = Fernet(symmetric_key).decrypt(encrypted_archive_bytes)

    # Store the decrypted archive
    decrypted_archive = f"{os.path.join(tmp_dir, name)}_TMP.zip"
    with open(decrypted_archive, "xb") as dst_file:
        dst_file.write(archive_bytes)

    extract_files(decrypted_archive, destination)


def decrypt_symmetric_key(private_key_bytes, symmetric_key_path, pw=None):
    """Decrypts a symmetric key using a private key.

    Args:
        private_key_bytes (bytes): The private key as bytes.
        symmetric_key_path (str): The path to the encrypted symmetric key.
        pw (Optional[str]): The password used to decrypt the private key.

    Returns:
        bytes: The decrypted symmetric key.
    """

    with open(symmetric_key_path, "rb") as symmetric_key_file:
        encrypted_symmetric_key = symmetric_key_file.read()

    private_key = load_private_key(private_key_bytes, pw)

    # Decrypt the symmetric key
    symmetric_key_bytes = private_key.decrypt(
        encrypted_symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA512()),
            algorithm=hashes.SHA512(),
            label=None,
        ),
    )

    return symmetric_key_bytes
