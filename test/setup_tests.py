"""Shared logic for setting up test cases."""

import os
from shutil import rmtree
from unittest import TestCase

from db import Archive, init_db, KeyPair, Password

NAME_1 = "NAME_1"
NAME_2 = "NAME_2"
TEST_DIR_DST = "TEST_DIR_DST"
TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_PATH_DST = os.path.join(TEST_PATH, TEST_DIR_DST)
SRC_FILE = os.path.join(TEST_PATH_DST, "TEST.txt")


class TestSetup(TestCase):
    """Generic setup and teardown implementation for common test data."""

    @classmethod
    def setUpClass(cls):
        """Creates an in memory DB for testing and a test path."""

        # Initialize an in memory DB
        init_db(":memory:")

        # Generate a password metadata object
        pw = Password(hint="test", strong=False)

        # Create a key pair, one with a password and one without
        KeyPair.create(
            name=NAME_1, public_key="", private_key="", password=None
        )
        KeyPair.create(name=NAME_2, public_key="", private_key="", password=pw)

        # Create archive metadata using each of the key pairs
        Archive.create(
            name=NAME_1,
            src_path="src",
            dst_path="dst",
            key_pair=KeyPair.select()
            .where(KeyPair.name == NAME_1)
            .execute()[0],
        )
        Archive.create(
            name=NAME_2,
            src_path="src",
            dst_path="dst",
            key_pair=KeyPair.select()
            .where(KeyPair.name == NAME_1)
            .execute()[0],
        )

        # Make a file and a directory used for testing
        try:
            os.mkdir(TEST_PATH_DST)
            if not os.path.exists(SRC_FILE):
                with open(SRC_FILE, "w+") as f:
                    f.write("TESTING")
        except FileExistsError as e:
            print(f"File Exists : {e}")

    @classmethod
    def tearDownClass(cls):
        """Removes the dummy directory used for testing."""
        rmtree(TEST_PATH_DST)
