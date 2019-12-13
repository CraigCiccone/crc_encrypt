"""Test validation related functions."""

from unittest import TestCase

from config import PW_MSG
from utils.validation import strong_password, validate_required

PW_FAIL = "pass"
PW_SHORT = "password"
PW_LOWER = "PASSWORDPASSWORDPASS"
PW_UPPER = "passwordpasswordpass"
PW_DIGITS = "PASSWORDPASSWORDpass"
PW_SPECIAL = "PASSWORDpassword1234"
PW_STRONG = "PASSWORDpassword12#$"


class TestValidation(TestCase):
    """Test functions in utils.validation."""

    def test_strong_pw(self):
        """Ensure strong_password properly evaluates pw strength."""

        # Test various dummy passwords
        pw_fail = strong_password(PW_FAIL)
        pw_short = strong_password(PW_SHORT)
        pw_lower = strong_password(PW_LOWER)
        pw_upper = strong_password(PW_UPPER)
        pw_digits = strong_password(PW_DIGITS)
        pw_special = strong_password(PW_SPECIAL)
        pw_strong = strong_password(PW_STRONG)

        # Validate what passwords are successful
        self.assertFalse(pw_fail.success)
        self.assertTrue(pw_short.success)
        self.assertTrue(pw_lower.success)
        self.assertTrue(pw_upper.success)
        self.assertTrue(pw_digits.success)
        self.assertTrue(pw_special.success)
        self.assertTrue(pw_strong.success)

        # Validate the corresponding message for the password's strength
        self.assertEqual(pw_fail.msg, PW_MSG["fail"])
        self.assertEqual(pw_short.msg, PW_MSG["short"])
        self.assertEqual(pw_lower.msg, PW_MSG["lower"])
        self.assertEqual(pw_upper.msg, PW_MSG["upper"])
        self.assertEqual(pw_digits.msg, PW_MSG["digits"])
        self.assertEqual(pw_special.msg, PW_MSG["special"])
        self.assertEqual(pw_strong.msg, "")

    def test_validate_required(self):
        """Ensure validate_required properly checks keyword arguments."""
        success = validate_required(a="a", b="b", c="c")
        fail = validate_required(a="a", b=None, c="c")
        self.assertTrue(success.success)
        self.assertFalse(fail.success)
