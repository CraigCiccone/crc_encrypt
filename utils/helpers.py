"""General helper functions."""

import os
from collections import namedtuple
from shutil import rmtree

from peewee import DoesNotExist
from kivy.utils import platform

from config import TABLE_SIZE_FACTOR, TABLE_SIZE_FACTOR_MOBILE, TMP_DIR
from db import Archive, KeyPair


#: Named tuple used to propagate results from function calls
Result = namedtuple("Result", ["success", "msg"])


def cleanup(destination):
    """Remove a temporary directory and any files in it.

    Args:
        destination (str): The path where the temporary directory was created.
    """
    tmp_dir = os.path.join(destination, TMP_DIR)
    if os.path.exists(tmp_dir):
        rmtree(tmp_dir)


def get_key_pairs():
    """Fetch all key pairs from the database.

    Returns:
        list[dict[str, str]]: All key pairs as a list of strings.
    """

    results = []
    key_pairs = KeyPair.select().order_by(KeyPair.timestamp.desc())

    for key_pair in key_pairs:

        # Set defaults for key pairs as they may not have a password
        name = key_pair.name
        password = "False"
        hint = ""
        strong = ""

        # Set password parameters if present
        if key_pair.password:
            password = "True"
            hint = key_pair.password.hint
            strong = str(key_pair.password.strong)

        results.append(
            {
                "name": name,
                "pw": password,
                "hint": hint,
                "strong": strong,
                "timestamp": str(key_pair.timestamp),
            }
        )

    return results


def get_key_names():
    """Fetch only the names of each key pair.

    Returns:
        list[str]: The names of all key pairs.
    """
    key_pairs = KeyPair.select().order_by(KeyPair.timestamp.desc())
    return [key_pair.name for key_pair in key_pairs]


def gui_thread(gui, func, err_msg, clean, **kwargs):
    """Run as a thread to execute another function asynchronously.

    Args:
        gui (RunGUI): The GUI for the application.
        func (function): The function to be executed.
        err_msg (str): An error message in case on any exceptions.
        clean (str): A temporary data location that needs to be removed.
        kwargs (str): All of the functions arguments as keyword arguments.
    """

    # Convert the keyword arguments to standard positional arguments
    args = tuple(kwargs.values())

    try:
        # Run the function with the provided args
        result = func(*args)

        # Update the GUI's combo boxes as new key pairs may have been added
        gui.update_drop_downs()

        # Check if a message needs to be shown to the end user
        if not result.success:
            gui.launch_popup("Error", f"{result.msg}", error=True)
            gui.popup_msg.dismiss()
        elif result.msg:
            gui.launch_popup("Warning", result.msg, error=True)
            gui.popup_msg.dismiss()

        # Cleanup temporary storage if needed
        if clean:
            cleanup(clean)

    except DoesNotExist:
        name = kwargs["key_pair_name"]
        gui.launch_popup(
            "Error", f'Key pair with name "{name}" does not exist', error=True
        )
        gui.popup_msg.dismiss()
    except Exception as e:
        gui.launch_popup("Error", f"{err_msg} -- {e}", error=True)
        gui.popup_msg.dismiss()
        if clean:
            cleanup(clean)

    # Re-enable submit buttons in the GUI upon function execution completion
    gui.enable_submits()


def get_table_width(data):
    """Determine the width of a GUI table based on the largest row.

    The maximum size is increased based on a predefined size factor to improve
    the overall look of the table.

    Args:
        data (list[dict[str, str]]): The table's data elements.

    Returns:
        int: The width of the table.
    """
    maximum = 0
    for row in data:
        length = 0
        for _, val in row.items():
            length += len(val)
        maximum = length if length > maximum else maximum

    # Set the width based on the target platform
    if platform == "android":
        return maximum * TABLE_SIZE_FACTOR_MOBILE
    else:
        return maximum * TABLE_SIZE_FACTOR


def get_archives():
    """Fetch all archives from the database.

    Returns:
        list[dict[str, str]]: All key pairs as a list of strings.
    """
    archives = Archive.select().order_by(Archive.timestamp.desc())
    data = []

    for archive in archives:
        data.append(
            {
                "name": archive.name,
                "src_path": archive.src_path,
                "dst_path": archive.dst_path,
                "kp": archive.key_pair.name,
                "timestamp": str(archive.timestamp),
            }
        )

    return data
