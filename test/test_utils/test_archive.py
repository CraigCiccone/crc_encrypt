"""Test archive related functions."""

import os
from shutil import rmtree
from unittest import TestCase

from utils.archive import extract_files, zip_dir, zip_files


TEST_DIR_SRC = "TEST_ARCH_SRC"
TEST_DIR_DST = "TEST_ARCH_DST"
TEST_FILE_NAME = "TEST_FILE.txt"
TEST_MSG = "THIS IS ONL A TEST"
TEST_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_PATH_DST = os.path.join(TEST_PATH, "..", TEST_DIR_DST)
TEST_PATH_SRC = os.path.join(TEST_PATH, "..", TEST_DIR_SRC)
TEST_PATH_FILE = os.path.join(TEST_PATH_SRC, TEST_FILE_NAME)
ZIP_FILE = "TEST_FILE.zip"
ZIP_DIR = "TEST_DIR.zip"


class TestArchive(TestCase):
    """Test functions in utils.archive."""

    @classmethod
    def setUpClass(cls):
        """Create dummy files for testing."""

        # Create dummy directories and files for testing
        os.mkdir(TEST_PATH_DST)
        os.mkdir(TEST_PATH_SRC)

        # Populate a dummy file with data
        with open(TEST_PATH_FILE, "w+") as f:
            f.write(TEST_MSG)

    @classmethod
    def tearDownClass(cls):
        """Remove dummy files used for testing."""
        rmtree(TEST_PATH_DST)
        rmtree(TEST_PATH_SRC)

    def test_zip_dir(self):
        """Ensure zip_dir creates a valid archive."""
        zip_dir(ZIP_DIR, TEST_PATH_SRC, TEST_PATH_DST)
        path = os.path.join(TEST_PATH_DST, ZIP_DIR)
        self.assertTrue(os.path.isfile(path))

    def test_zip_files(self):
        """Test both zip_files and extract_files.

        Ensure zip_files creates a valid archive and that extract_files
        extracts it successfully.
        """

        # Test zip_files
        zip_files(ZIP_FILE, [TEST_PATH_FILE], TEST_PATH_DST)
        path = os.path.join(TEST_PATH_DST, ZIP_FILE)
        self.assertTrue(os.path.isfile(path))

        # Test extract_files
        extract_files(path, TEST_PATH_DST)
        result = os.path.join(TEST_PATH_DST, TEST_FILE_NAME)
        with open(result, "r") as f:
            text = f.read()
        self.assertEqual(text, TEST_MSG)
