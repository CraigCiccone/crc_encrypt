"""Test helper functions."""

import os

from config import TMP_DIR
from test.setup_tests import TestSetup, TEST_PATH_DST
from utils.helpers import (
    cleanup,
    get_archives,
    get_key_names,
    get_key_pairs,
    get_table_width,
)


class TestHelpers(TestSetup):
    """Test functions in utils.helpers."""

    def test_cleanup(self):
        """Ensure cleanup removes a temporary directory successfully."""
        temp = os.path.join(TEST_PATH_DST, TMP_DIR)
        os.mkdir(temp)
        cleanup(TEST_PATH_DST)
        self.assertEqual(False, os.path.isdir(temp))

    def test_get_archives(self):
        """Ensure get_archives returns the expected data."""
        result = get_archives()
        self.assertEqual(len(result), 2)

    def test_get_key_names(self):
        """Ensure get_key_names returns the expected data."""
        result = get_key_names()
        self.assertEqual(len(result), 2)

    def test_get_table_width(self):
        """Ensure get_table_width returns a valid integer greater than 0."""
        result_keys = get_table_width(get_key_pairs())
        result_archives = get_table_width(get_archives())
        self.assertGreater(result_keys, 0)
        self.assertGreater(result_archives, 0)

    def test_validate_required(self):
        """Ensure get_key_pairs returns the expected data."""
        result = get_key_pairs()
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 5)
