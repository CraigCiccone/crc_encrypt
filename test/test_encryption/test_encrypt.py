"""Test functions related to encryption."""

import os

from config import DB_PATH
from encryption.decrypt import decrypt_archive, db_restore_wrapper
from encryption.encrypt import db_backup_wrapper, encrypt_wrapper
from encryption.keys import generate_asymmetric_key_pair
from test.setup_tests import SRC_FILE, TestSetup, TEST_PATH_DST
from utils.helpers import cleanup


class TestEncrypt(TestSetup):
    """Tests the functionality in the encryption package."""

    def test_encryption(self):
        """Ensure encryption, decryption, DB backups, and DB restores work."""

        # Test encryption
        kp_name = "Testing"
        pw = "password"
        path_enc = os.path.join(TEST_PATH_DST, "ENC")
        os.mkdir(path_enc)
        generate_asymmetric_key_pair(kp_name, pw=pw)
        result_enc = encrypt_wrapper(SRC_FILE, path_enc, kp_name)
        self.assertEqual(result_enc.success, True)
        self.assertEqual(result_enc.msg, "")

        # Test decryption
        file_path = os.path.join(path_enc, "TEST.txt.zip")
        path_dec = os.path.join(TEST_PATH_DST, "DEC")
        os.mkdir(path_dec)
        result_dec = decrypt_archive(file_path, path_dec, kp_name, pw=pw)
        self.assertEqual(result_dec.success, True)
        self.assertEqual(result_dec.msg, "")

        # Test DB backup
        path_db = os.path.join(TEST_PATH_DST, "DB")
        os.mkdir(path_db)
        result_db = db_backup_wrapper(path_db, kp_name)
        self.assertEqual(result_db.success, True)

        # Test DB restore
        path_back = os.path.join(path_db, "crc_encrypt.db.zip")
        result_back = db_restore_wrapper(path_back, pw)
        self.assertEqual(result_back.success, True)
        self.assertEqual(result_back.msg, "")
        cleanup(DB_PATH)
