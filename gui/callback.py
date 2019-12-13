"""GUI call back functions and related helper functions."""

from functools import partial
from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.modalview import ModalView
from kivy.uix.rst import RstDocument
from kivy.uix.popup import Popup
from kivy.utils import platform

from config import HELP_TXT, RESIZE_LIMIT
from gui.table import ArchiveRecycleView, KeysRecycleView


def archives_cb(_caller):
    """Call back function for the Action Bar's 'Archive' button.

    This launches a full screen popup containing a table that displays archive
    meta data.

    Args:
        _caller (Widget): Widget that triggered this function.
    """
    popup = Popup(title="Archive Metadata", auto_dismiss=False)
    build_table_layout(ArchiveRecycleView(), popup)
    popup.open()


def build_table_layout(table, popup):
    """Builds a standard layout to present table based data.

    The layout consists of a table and a close button presented via a popup
    window.

    Args:
        table (Union[ArchiveRecycleView, KeysRecycleView]): The table object.
        popup (Popup): Popup window that will show the table.
    """

    # Orient the overall layout vertically
    main_layout = BoxLayout(orientation="vertical")
    main_layout.add_widget(table)

    # Create a horizontal sub-layout for the close button
    sub_layout = BoxLayout(orientation="horizontal")
    sub_layout.size_hint_y = None
    sub_layout.height = "30dp"
    button = Button(text="Close")

    # Set the widgets
    sub_layout.add_widget(button)
    main_layout.add_widget(sub_layout)

    # Set the close button to dismiss the popup
    button.bind(on_press=popup.dismiss)
    popup.content = main_layout


def file_cb(input_text, _instance):
    """Call back function to select a file or directory on the file system.

    The selected file or directory is subsequently populated in the provided
    input_text field.

    Args:
        input_text (TextInput): Populated by the selection.
        _instance (Widget): Required Kivy bind parameter.
    """

    # Initialize a file chooser in the user's home directory
    file_choose = FileChooserIconView()

    # Set the initial directory based on the platform
    if platform == "android":
        file_choose.path = "/storage/emulated/0"
    else:
        file_choose.path = str(Path.home())

    # Allow directory selection and configure the file chooser's scrolling
    file_choose.dirselect = True
    file_choose.layout.ids.scrollview.scroll_type = ["bars", "content"]
    file_choose.layout.ids.scrollview.bar_width = "12dp"
    file_choose.bind()

    # Set the layout for the popup window including a "Select" button. This
    # button is bound to another function to process the file chooser value
    main_layout = BoxLayout(orientation="vertical")
    main_layout.add_widget(file_choose)
    sub_layout = BoxLayout(orientation="horizontal")
    sub_layout.size_hint_y = None
    sub_layout.height = "30dp"
    select = Button(text="Select")
    cancel = Button(text="Cancel")
    sub_layout.add_widget(select)
    sub_layout.add_widget(cancel)
    main_layout.add_widget(sub_layout)

    # Initialize and open the popup that presents the file chooser
    popup = Popup(title="File Chooser", auto_dismiss=False)
    select.bind(
        on_release=partial(file_result_cb, file_choose, popup, input_text)
    )
    cancel.bind(on_release=popup.dismiss)
    popup.content = main_layout
    popup.open()


def file_result_cb(file_chooser, popup, input_text, _instance):
    """Callback function to set an input_text value from a file_chooser.

    The input_text value is only set if a selection is made by the user.

    Args:
        file_chooser (FileChooserIconView): File chooser.
        popup (Popup): Popup that closes upon value selection.
        input_text (TextInput): Populated by the selection.
        _instance (Widget): Required Kivy bind parameter.
    """
    if len(file_chooser.selection) > 0:
        input_text.text = file_chooser.selection[0]
    popup.dismiss()


def help_cb(_caller):
    """Call back function for the Action Bar's 'Help' button.

    This launches a modal containing a reST document with help information.

    Args:
        _caller (Widget): Widget that triggered this function.
    """

    # Establish the help layout
    main_layout = BoxLayout(orientation="vertical")
    sub_layout = BoxLayout(orientation="horizontal")
    sub_layout.size_hint_y = None
    sub_layout.height = "32dp"

    # Set a close button
    button = Button(text="Close")
    sub_layout.add_widget(button)

    # Add the help information
    main_layout.add_widget(
        RstDocument(
            text=HELP_TXT, scroll_type=["bars", "content"], bar_width="12dp"
        )
    )
    main_layout.add_widget(sub_layout)

    # Bind and launch the popup
    popup = ModalView(
        size_hint=(None, None), size=("350dp", "300dp"), auto_dismiss=False
    )
    button.bind(on_release=popup.dismiss)
    popup.add_widget(main_layout)
    popup.open()


def key_pairs_cb(_caller):
    """Call back function for the Action Bar's 'Key Pairs' button.

    This launches a full screen popup containing a table that displays key pair
    meta data.

    Args:
        _caller (Widget): Widget that triggered this function.
    """
    popup = Popup(title="Key Pair Metadata", auto_dismiss=False)
    build_table_layout(KeysRecycleView(), popup)
    popup.open()


def win_resize_cb(app, _window, _width, height):
    """Adjusts splitter height when the Kivy window size changes.

    Upon a window resize event each tab's help information splitter height is
    altered to match the window height.

    Args:
        app (AppGUI): The GUI application.
        _window (Window): The Kivy window object. It is not used.
        _width (int): The width of the GUI window. It is not used.
        height (int): The height of the GUI window.
    """
    if height > RESIZE_LIMIT:
        app.encrypt_tab.splitter.height = height
        app.decrypt_tab.splitter.height = height
        app.generate_tab.splitter.height = height
        app.db_backup_tab.splitter.height = height
        app.db_restore_tab.splitter.height = height
        app.import_tab.splitter.height = height
        app.export_tab.splitter.height = height
        app.export_all_tab.splitter.height = height
