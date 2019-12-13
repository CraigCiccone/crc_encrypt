"""CLI related functions."""

from click import group, option, Path
from getpass import getpass
from peewee import DoesNotExist

from config import DB_PATH, HELP
from db import Archive
from encryption.decrypt import db_restore_wrapper, decrypt_archive
from encryption.encrypt import db_backup_wrapper, encrypt_wrapper
from encryption.keys import (
    generate_asymmetric_key_pair,
    import_key_pair,
    write_all_key_pairs,
    write_key_pair,
)
from utils.helpers import cleanup, get_key_pairs


@group()
def main():
    """CRC Encrypt CLI"""
    pass


@main.command()
@option("-d", "--destination", type=Path(), required=True, help=HELP["dst"])
@option("-k", "--key_pair_name", type=str, required=True, help=HELP["kp"])
def db_backup(destination, key_pair_name):
    """Creates an encrypted backup of the database."""
    try:
        db_backup_wrapper(destination, key_pair_name)
        cleanup(destination)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(destination)


@main.command()
@option("-s", "--source", type=str, required=True, help=HELP["src_file"])
def db_restore(source):
    """Restores the database from a backup."""
    password = getpass()
    try:
        db_restore_wrapper(source, password)
        cleanup(DB_PATH)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(DB_PATH)


@main.command()
@option("-s", "--source", type=str, required=True, help=HELP["src_file"])
@option("-d", "--destination", type=Path(), required=True, help=HELP["dst"])
@option("-k", "--key_pair_name", type=str, required=True, help=HELP["kp"])
@option("-p", "--password", is_flag=True, help=HELP["pw"])
def decrypt(source, destination, key_pair_name, password):
    """Decrypts an archive."""
    pw = ""
    if password:
        pw = getpass()
    try:
        decrypt_archive(source, destination, key_pair_name, pw)
        cleanup(destination)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(destination)


@main.command()
@option("-s", "--source", type=str, required=True, help=HELP["src"])
@option("-d", "--destination", type=Path(), required=True, help=HELP["dst"])
@option("-k", "--key_pair_name", type=str, required=True, help=HELP["kp"])
def encrypt(source, destination, key_pair_name):
    """Encrypts a file or directory."""
    try:
        encrypt_wrapper(source, destination, key_pair_name)
        cleanup(destination)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(destination)


@main.command()
@option("-d", "--destination", type=Path(), required=True, help=HELP["dst"])
def export_all_keys(destination):
    """Exports all key pairs."""
    write_all_key_pairs(destination)


@main.command()
@option("-k", "--key_pair_name", type=str, required=True, help=HELP["kp"])
@option("-d", "--destination", type=Path(), required=True, help=HELP["dst"])
def export_key(key_pair_name, destination):
    """Exports a specific key pair."""
    write_key_pair(key_pair_name, destination)


@main.command()
@option("-k", "--key_pair_name", type=str, required=True, help=HELP["kp"])
@option("-h", "--hint", type=str, help=HELP["hint"])
@option("-p", "--password", is_flag=True, help=HELP["pw"])
def generate(key_pair_name, hint, password):
    """Generates a new asymmetric key pair set."""
    pw = ""
    if password:
        pw = getpass()
        confirm = getpass("Confirm: ")
        if pw != confirm:
            print("Password entries do not match")
            return
    generate_asymmetric_key_pair(key_pair_name, hint, pw)


@main.command()
@option("-k", "--key_pair_name", type=str, required=True, help=HELP["kp"])
@option("-pr", "--private_key", type=str, required=True, help=HELP["priv"])
@option("-pu", "--public_key", type=str, required=True, help=HELP["pub"])
@option("-h", "--hint", type=str, help=HELP["hint"])
@option("-pw", "--password", is_flag=True, help=HELP["pw"])
def import_key(key_pair_name, private_key, public_key, hint, password):
    """Imports a specific key pair."""
    pw = ""
    if password:
        pw = getpass()
    import_key_pair(key_pair_name, private_key, public_key, hint, pw)


@main.command()
def show_all_archives():
    """Displays meta data for all archives."""

    archives = Archive.select()
    template = "{: <32} {: <64} {: <64} {: <32} {: <32}"
    header = [
        "Name",
        "Source Path",
        "Destination Path",
        "Key Pair Name",
        "Timestamp",
    ]

    print(template.format(*header))
    for archive in archives:
        row = [
            archive.name[:32],
            archive.src_path[:64],
            archive.dst_path[:64],
            archive.key_pair.name,
            str(archive.timestamp),
        ]
        print(template.format(*row))


@main.command()
@option("-a", "--archive_name", type=str, required=True, help=HELP["arch"])
def show_archive(archive_name):
    """Displays meta data for a specific archive."""

    try:
        archive = Archive.get(Archive.name == archive_name)
    except DoesNotExist:
        print(f"Archive does not exist : {archive_name}")
        return

    # Set default password information
    key_pair = archive.key_pair
    password = "False"
    hint = ""
    strong = ""

    # Set actual password information if present
    if key_pair.password:
        password = "True"
        hint = key_pair.password.hint
        strong = str(key_pair.password.strong)

    print(f"Name             : {archive.name}")
    print(f"Source Path      : {archive.src_path}")
    print(f"Destination Path : {archive.dst_path}")
    print(f"Key Pair Name    : {key_pair.name}")
    print(f"Password         : {password}")
    print(f"Password Hint    : {hint}")
    print(f"Strong Password  : {strong}")
    print(f"Timestamp        : {archive.timestamp}")


@main.command()
def show_keys():
    """Displays meta data for all key pairs."""

    key_pairs = get_key_pairs()
    template = "{: <32} {: <10} {: <64} {: <16} {: <32}"
    header = [
        "Name",
        "Password",
        "Password Hint",
        "Strong Password",
        "Timestamp",
    ]

    print(template.format(*header))
    for key_pair in key_pairs:
        key_pair_list = [
            key_pair["name"],
            key_pair["pw"],
            key_pair["hint"],
            key_pair["strong"],
            key_pair["timestamp"],
        ]
        print(template.format(*key_pair_list))
