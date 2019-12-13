"""Entry point into the application."""

import sys

from cli import main
from config import DB, DB_FILE_PATH
from db import db_exists, init_db


if __name__ == "__main__":

    # Create the DB if it does not exist
    if not db_exists():
        init_db(DB_FILE_PATH)

    # Connect to the DB
    DB.init(DB_FILE_PATH)

    # Run the CLI if command line arguments are present
    if len(sys.argv) > 1:
        main()
    else:
        # Import here to set Kivy's config before the window launches
        from kivy.config import Config
        from kivy.utils import platform

        # Set Kivy's window size and disable mouse based touch emulation
        Config.set("graphics", "width", "764")
        Config.set("graphics", "height", "475")
        Config.set("graphics", "minimum_width", "764")
        Config.set("graphics", "minimum_height", "475")

        # Do not alter the input config for android
        if platform != "android":
            Config.set("input", "mouse", "mouse,multitouch_on_demand")

        # Import the Kivy application here to prevent the window from opening
        from gui.app import AppGUI

        # Hide the console in GUI mode on Windows
        if sys.platform.lower().startswith("win"):
            import ctypes

            window = ctypes.windll.kernel32.GetConsoleWindow()
            if window != 0:
                ctypes.windll.user32.ShowWindow(window, 0)

        AppGUI().run()
