CRC Encrypt
===========
This application allows you to encrypt files or directories for secure storage.
It combines both symmetric and asymmetric cryptography for an efficient and
secure encryption implementation. Encryption keys are managed by the
application and stored in a local SQLite database.

The application has both a graphical interface and a CLI. All application
functionality is available in either the GUI or the CLI.

Warnings
--------
Password information is not stored within this application. You must remember
your passwords. There is no way to restore a forgotten password.

Private keys are intended to be just that, private. Be aware that if you share
a private key that is not password protected, then anyone who has access to
that private key can decrypt your data.

The following password criteria is recommended for a strong password:

* 20 or more characters long
* 2 or more lowercase letters (a-z)
* 2 or more uppercase letters (A-Z)
* 2 or more digits (0-9)
* 2 or more special characters:  !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~

Note that the space character ( ) is included in the special characters.

Install
-------

1. Navigate to the releases_ section.
2. Download the release that corresponds to your operating system.
3. Extract the zip archive.
4. Run the executable.

If installing on Android, you must go to Settings -> Apps -> CRC Encrypt ->
Permissions and grant *Storage* permissions to properly browse the file system.

Build
-----
The easiest way to get started is via the releases_, but the application can be
built from source if needed. The recommended Python version for building this
application is 3.7; however, any version greater than 3.6 should be
sufficient.

**Windows**

.. code-block:: text

    git clone https://github.com/ProtoInfinite/crc_encrypt.git
    pip install -r crc_encrypt\requirements\requirements.txt
    pip install -r crc_encrypt\requirements\requirements_win.txt
    pip install -r crc_encrypt\requirements\requirements_build.txt
    python -m PyInstaller --name crc_encrypt crc_encrypt\main.py

Add the following near the top of crc_encrypt.spec:

.. code-block:: python

    from kivy_deps import sdl2, glew

Edit (near the bottom) crc_encrypt.spec to match the following:

.. code-block:: python

    coll = COLLECT(exe, Tree('path\\to\\crc_encrypt\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='crc_encrypt')

Finally build the executable:

.. code-block:: python

    python -m PyInstaller crc_encrypt.spec

**Linux**

.. code-block:: text

    git clone https://github.com/ProtoInfinite/crc_encrypt.git
    pip install -r crc_encrypt/requirements/requirements.txt
    pip install -r crc_encrypt/requirements/requirements_build.txt
    python -m PyInstaller --name crc_encrypt crc_encrypt/main.py

Edit (near the bottom) crc_encrypt.spec to match the following:

.. code-block:: python

    coll = COLLECT(exe, Tree('path/to/crc_encrypt/'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='crc_encrypt')

Finally build the executable:

.. code-block:: python

    python -m PyInstaller crc_encrypt.spec

**Android**

These build steps must be run on Linux. Note that Android build times can take
a significant amount of time.

If Java (JDK 8) is not already installed, you must install it prior to building
for Android.

.. code-block:: text

    git clone https://github.com/ProtoInfinite/crc_encrypt.git
    pip install -r crc_encrypt/requirements/requirements.txt
    pip install -r crc_encrypt/requirements/requirements_build.txt
    buildozer init

Edit the following fields in the generated buildozer.spec file:

.. code-block:: python

    # (str) Title of your application
    title = CRC Encrypt

    # (str) Package name
    package.name = crc_encrypt

    # (str) Package domain (needed for android/ios packaging)
    package.domain = org.crc

    # (list) Application requirements
    # comma separated e.g. requirements = sqlite3,kivy
    requirements = python3,kivy,sqlite3,click,cryptography,peewee,docutils

    # (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
    orientation = all

    # (list) Permissions
    android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

Finally, build the Android apk. This is the step that will take a significant
amount of time.

.. code-block:: text

    buildozer -v android debug

If you run into dependency issues, refer to buildozer's Dockerfile and
buildozer's latest documentation:

* https://github.com/kivy/buildozer/blob/master/Dockerfile
* https://buildozer.readthedocs.io/en/latest/installation.html

To debug the build on an Android device connected via USB, run the following:

.. code-block:: text

    buildozer -v android deploy run logcat

**iOS and OSX**

There are no plans to support builds for iOS or OSX. However, it should be
possible to build for either platform. Consult these resources:

* https://kivy.org/doc/stable/guide/packaging-ios.html
* https://kivy.org/doc/stable/guide/packaging-osx.html

Standard Tutorials
==================

Generate a New Key Pair
-----------------------

1. Navigate to the **Generate** tab.
2. Provide a unique name for the new key pair.
3. Press the submit button.

You can see your new key pair in the **Keys** table.

Note that you can optionally secure the private key with a password. It is
highly recommended to secure the private key with a password. If you forget
your password, you can review your password hint via the **Keys** table.

Encrypt Files or Folders
------------------------
Ensure you have already generated a new key pair.

1. Navigate to the **Encrypt** tab.
2. Select your key pair from the drop down.
3. Choose the file or folder to encrypt via the source browse button.
4. Choose where to store the encrypted data via the destination browse button.
5. Press the submit button.

Your encrypted data will be stored in a zip file in the selected destination.

Decrypt Files or Folders
------------------------
Ensure you know which key pair you used to encrypt the archive before starting.
Also ensure that you know the password used to secure the key pair if a
password was used. If you are unsure if a key pair has a password, see the
**Keys** table.

1. Navigate to the **Decrypt** tab.
2. Choose the encrypted archive via the source browse button.
3. Choose where to put the unencrypted data via the destination browse button.
4. Provide a password if a password is associated with the key pair.
5. Press the submit button.

Your original source data will be present in the selected destination.

Advanced Tutorials
==================

Backup the Database
-------------------
Database backups are encrypted as they hold private key information. You must
have a key pair that is secured with a password to backup the database. A
strong password is highly recommended as the private key used to encrypt the
database backup is stored alongside the backup.

1. Navigate to the **DB Backup** tab.
2. Select the key pair to encrypt the backup from the dropdown.
3. Choose where to put the encrypted backup via the destination browse button.
4. Press the submit button.

Your encrypted database backup will be stored in a zip file in the selected
destination.

Note that it is not recommended to backup the database by simply copying the
database file (crc_encrypt.db) which is not encrypted and therefore can expose
private key information.

Restore the Database
--------------------
Note that an unencrypted copy of the database is made prior to attempting to
restore the database from an encrypted backup. This file will be named
crc_encrypt.db.back_# and can be renamed to crc_encrypt.db to restore this
unencrypted backup.

1. Navigate to the **DB Restore** tab.
2. Choose the database backup to restore via the source browse button.
3. Provide the password used to secure the private key encrypting the backup.
4. Press the submit button.

The database will automatically be restored from the backup.

Import a Key Pair
-----------------
It is only recommended to import key pairs that were made with this
application.

1. Navigate to the **Import** tab.
2. Give the key pair a unique name.
3. Select the private key file via the private key browse button.
4. Select the public key file via the public key browse button.
5. Optionally provide a password hint to remember the key's password.
6. Provide a password if the key is secured with a password.
7. Press the submit button.

THe key pair will automatically be added to the database. You can view
information about the key in the **Keys** table.

Export Key Pairs
----------------
Keys can be exported individually or all at once. This guide will show a single
key export.

1. Navigate to the **Export** tab.
2. Select the key pair to export from the dropdown.
3. Choose where to store the exported key via the destination browse button.
4. Press the submit button.

Note that all keys can be exported at once via the **Export All** tab. Also
note that keys are exported in PEM format.

CLI
---
To utilize the application via the CLI, please follow the help instructions
provided by the CLI itself:

**Windows**

.. code-block:: text

    crc_encrypt.exe --help

**Linux**

.. code-block:: text

    ./crc_encrypt --help


.. Links used in this document
.. _releases: https://github.com/ProtoInfinite/crc_encrypt/releases
