"""Test functions related to symmetric and asymmetric keys."""

import os

from db import KeyPair
from encryption.keys import (
    generate_asymmetric_key_pair,
    import_key_pair,
    write_all_key_pairs,
)
from test.setup_tests import TestSetup, TEST_PATH_DST

NAME = "TEST_PAIR"
NEW_NAME = "NEW_TEST_PAIR"


class TestKeys(TestSetup):
    """Test functions in encryption.keys."""

    def test_key_pairs(self):
        """Ensure keys are generated, imported and exported successfully."""

        # Generate a key
        generate_asymmetric_key_pair(NAME)
        kp = KeyPair.select().where(KeyPair.name == NAME).execute()[0]
        self.assertEqual(kp.name, NAME)
        self.assertIsNotNone(kp.private_key)
        self.assertIsNotNone(kp.public_key)

        # Export the keys
        result_exp = write_all_key_pairs(TEST_PATH_DST)
        self.assertEqual(result_exp.success, True)
        self.assertEqual(result_exp.msg, "")

        # Import a key
        priv_path = os.path.join(TEST_PATH_DST, NAME, f"{NAME}_PRIVATE.key")
        pub_path = os.path.join(TEST_PATH_DST, NAME, f"{NAME}_public.key")
        result_imp = import_key_pair(NEW_NAME, priv_path, pub_path)
        self.assertEqual(result_imp.success, True)
        self.assertEqual(result_imp.msg, "")
        kp = KeyPair.select().where(KeyPair.name == NEW_NAME).execute()[0]
        self.assertEqual(kp.name, NEW_NAME)
        self.assertIsNotNone(kp.private_key)
        self.assertIsNotNone(kp.public_key)
