"""Functions to validate user input."""

import re

from config import PW_MSG, SPECIAL_CHARS
from utils.helpers import Result


def strong_password(pw):
    """Determine the strength of a password based on a fixed criteria.

    Args:
        pw (str): The password to be tested for its strength.

    Returns:
        Result: Summary of whether or not the password is strong.
    """
    special = SPECIAL_CHARS
    success = True
    msg = ""

    # Perform regex operations that evaluate password strength criteria
    match_alpha_lower = re.findall("[a-z]", pw)
    match_alpha_upper = re.findall("[A-Z]", pw)
    match_digits = re.findall("[0-9]", pw)
    match_special = re.findall(f"[{special}]", pw)

    # Validates each portion of the password strength criteria
    if len(pw) < 8:
        msg = PW_MSG["fail"]
        success = False
        print(msg)
    elif len(pw) < 20:
        msg = PW_MSG["short"]
        print(msg)
    elif len(match_alpha_lower) < 2:
        msg = PW_MSG["lower"]
        print(msg)
    elif len(match_alpha_upper) < 2:
        msg = PW_MSG["upper"]
        print(msg)
    elif len(match_digits) < 2:
        msg = PW_MSG["digits"]
        print(msg)
    elif len(match_special) < 2:
        msg = PW_MSG["special"]
        print(msg)

    return Result(success, msg)


def validate_required(**kwargs):
    """Checks if a set of required arguments have any value.

    Args:
        kwargs: All of the arguments to be validated as keyword arguments.

    Returns:
        Result: This object's success attribute is True if all args have value.
    """
    result = True
    msg = "These parameters are required -- "

    for kwarg in kwargs:
        # Build an error message based on the required arguments
        msg = f'{msg}"{str(kwarg).title().replace("_", " ")}", '

        # Test the argument using its "truthiness"
        result = result and kwargs[kwarg]

    if result:
        return Result(result, "")

    return Result(result, msg[:-2])
