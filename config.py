"""Configurable parameters used by the application."""

import os

from peewee import SqliteDatabase


#: Valid special characters for passwords
SPECIAL_CHARS = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

# DB related parameters
DB_FILE = "crc_encrypt.db"
DB_PATH = os.path.dirname(os.path.abspath(__file__))
DB_FILE_PATH = os.path.join(DB_PATH, DB_FILE)
DB = SqliteDatabase(None)

#: Temporary directory name
TMP_DIR = "___tmp_crc_encrypt___"

# Strings appended to particular files
FILE_UNENCRYPTED = "_UNENCRYPTED.zip"
FILE_KEY = "_KEY.key"
FILE_CRYPT = "_ENCRYPTED.zip"
FILE_PUB = "_public.key"
FILE_PRIV = "_PRIVATE.key"

#: Help messages used in the CLI
HELP = {
    "kp": "The name used to identify the key pair.",
    "pw": "A boolean flag used to determine if a password is needed.",
    "hint": "A hint to help recall a password.",
    "src": "The path to the source file or directory.",
    "src_file": "The path to the source file.",
    "dst": "The directory path where the results will be stored.",
    "priv": "The path to the private key file.",
    "pub": "The path to the public key file.",
    "arch": "The file name of the archive.",
}

# GUI parameters
TABLE_SIZE_FACTOR = 14
TABLE_SIZE_FACTOR_MOBILE = 50

# Password strength messages
special_msg = "Passwords should have 2 or more special characters: "
PW_MSG = {
    "fail": "Passwords must be at least 8 characters long.",
    "short": "Passwords should be at least 20 characters long.",
    "lower": "Passwords should have 2 or more lowercase letters (a-z).",
    "upper": "Passwords should have 2 or more uppercase letters (A-Z).",
    "digits": "Passwords should have 2 or more digits (0-9)",
    "special": f"{special_msg}{SPECIAL_CHARS}",
}

# GUI reST template for the help message
HELP_TXT = f"""
General Help
=============
Detailed guides and instructions can be found here:
https://github.com/CraigCiccone/crc_encrypt

Password Strength
==================
The following criteria is recommended for a strong password:

- 20 or more characters long
- 2 or more lowercase letters (a-z)
- 2 or more uppercase letters (A-Z)
- 2 or more digits (0-9)
- 2 or more special characters: {SPECIAL_CHARS}
"""

# GUI reST template for general messages
INFO_TXT = """
{title:s}
===============================================
{msg:s}
"""

# Smallest height where the GUI will resize Kivy help splitters
RESIZE_LIMIT = 380

# GUI reST templates for each tab's help message
ENCRYPT_HELP = """
**Overview**

Encrypt a file or folder using an existing key pair.

**Note**

If a key pair has not been generated yet, navigate to the *Generate*
tab to create your first key pair.

**Values**

* *Key Pair Name* (Required) - Key pair for encryption and decryption
* *Source* (Required) - The file or folder to be encrypted
* *Destination* (Required) - Where the encrypted data will be stored
"""
DECRYPT_HELP = """
**Overview**

Decrypt a file or folder that has been encrypted with this application.

**Note**

The password field is needed only if the key pair used for encryption
was created with a password.

**Values**

* *Key Pair Name* (Required) - Key pair for encryption and decryption
* *Source* (Required) - The encrypted archive to be decrypted
* *Destination* (Required) - Where the decrypted data will be stored
* *Password* (Optional) - Password used to secure the key pair
"""
GENERATE_HELP = """
**Overview**

Creates a new key pair that can be used to encrypt data.

**Note**

Key pair names must be unique. A password is highly recommended for
additional security. See the *Help* section for information regarding
strong passwords.

**Values**

* *Key Pair Name* (Required) - The unique name for the key pair
* *Password Hint* (Optional) - Can help to remember the password
* *Password* (Optional) - Used to further secure the private key
* *Confirm Password* (Optional) - Confirmation of the password
"""
DB_BACKUP_HELP = """
**Overview**

Creates a backup of the database. The database backup is encrypted for
safe storage.

**Note**

The private key to decrypt the database backup is stored within the
database backup. For this reason, a password protected private key is
required.

**Values**

* *Key Pair Name* (Required) - Key pair used to encrypt the backup
* *Destination* (Required) - Where the backup will be stored
"""
DB_RESTORE_HELP = """
**Overview**

Restores the database from a backup.

**Note**

If you forget which key pair was used to backup the database, review
the *Archives* table which identifies the key pair used to secure the
database backup.

**Values**

* *Source* (Required) - The database backup to be restored.
* *Password* (Required) - Password used to secure the key pair
"""
IMPORT_HELP = """
**Overview**

Imports an existing key pair into this application.

**Note**

Only import key pairs that were generated using this application. A
password must be provided if the key was originally secured with a
password. Keys are expected to be in PEM format.

**Values**

* *Key Pair Name* (Required) - The unique name for the key pair
* *Private Key* (Required) - The private key file
* *Public Key* (Required) - The public key file
* *Password Hint* (Optional) - Can help to remember the password
* *Password* (Optional) - Used to further secure the private key
"""
EXPORT_HELP = """
**Overview**

Exports a key pair from this application into two files, one for the
private key and one for the public key.

**Note**

The keys are exported in PEM format.

**Values**

* *Key Pair Name* (Required) - Key pair to be exported
* *Destination* (Required) - Where the key pair will be stored
"""
EXPORT_ALL_HELP = """
**Overview**

Exports all key pairs from this application.

**Note**

Each key pair is stored in its own subdirectory of the destination in
PEM format.

**Values**

* *Destination* (Required) - Where the key pairs will be stored
"""
