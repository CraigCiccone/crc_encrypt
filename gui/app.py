"""The main Kivy based GUI application."""

from threading import Thread

from kivy.app import App
from kivy.uix.actionbar import (
    ActionBar,
    ActionButton,
    ActionView,
    ActionPrevious,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.rst import RstDocument
from kivy.uix.tabbedpanel import TabbedPanel

from config import DB_PATH, INFO_TXT
from encryption.decrypt import db_restore_wrapper, decrypt_archive
from encryption.encrypt import db_backup_wrapper, encrypt_wrapper
from encryption.keys import (
    generate_asymmetric_key_pair,
    import_key_pair,
    write_all_key_pairs,
    write_key_pair,
)
from gui.callback import archives_cb, help_cb, key_pairs_cb
from gui.tab import (
    DatabaseBackupTab,
    DatabaseRestoreTab,
    DecryptTab,
    EncryptTab,
    ExportAllTab,
    ExportTab,
    GenerateTab,
    ImportTab,
)
from utils.helpers import get_key_names, gui_thread
from utils.validation import validate_required


class AppGUI(App):
    """Kivy GUI based application.

    The application consists of an action bar with several links and dedicated
    tabs for each of the applications main functions. Each tab provides
    detailed help information via a Kivy Splitter.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        title (str): The window's title
        key_names (list[str]): All of the key pair names from the DB.
        popup_msg (ModalView): A popup that shows an informational message.
        popup_err (ModalView): A popup that shows a warning or error message.
        encrypt_tab (EncryptTab): The encrypt tab object.
        decrypt_tab (DecryptTab): The decrypt tab object.
        generate_tab (GenerateTab): The generate new keys tab object.
        db_backup_tab (DatabaseBackupTab): The DB backup tab object.
        db_restore_tab (DatabaseRestoreTab): The DB restore tab object.
        import_tab (ImportTab): The import a key tab object.
        export_tab (ExportTab): The export one key tab object.
        export_all_tab (ExportAllTab): The export all keys tab object.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = "CRC Encrypt"

        self.key_names = get_key_names()

        self.popup_msg = ModalView(
            size_hint=(None, None), size=("300dp", "200dp"), auto_dismiss=False
        )
        self.popup_err = ModalView(
            size_hint=(None, None), size=("300dp", "200dp"), auto_dismiss=False
        )

        self.encrypt_tab = EncryptTab(self.key_names, self.encrypt)
        self.decrypt_tab = DecryptTab(self.key_names, self.decrypt)
        self.generate_tab = GenerateTab(self.generate)
        self.db_backup_tab = DatabaseBackupTab(self.key_names, self.db_backup)
        self.db_restore_tab = DatabaseRestoreTab(self.db_restore)
        self.import_tab = ImportTab(self.import_key)
        self.export_tab = ExportTab(self.key_names, self.export_key)
        self.export_all_tab = ExportAllTab(self.export_all_keys)

    def encrypt(self, _instance):
        """Encrypt a file or folder using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            encrypt_wrapper,
            ["source", "destination", "key_pair_name"],
            "Failed to encrypt archive",
            "Encrypting Archive",
            clean=self.encrypt_tab.dst_txt.text,
            source=self.encrypt_tab.src_txt.text,
            destination=self.encrypt_tab.dst_txt.text,
            key_pair_name=self.encrypt_tab.spinner.text,
        )

    def decrypt(self, _instance):
        """Decrypt a file or folder using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            decrypt_archive,
            ["source", "destination", "key_pair_name"],
            "Failed to decrypt archive",
            "Decrypting Archive",
            clean=self.decrypt_tab.dst_txt.text,
            source=self.decrypt_tab.src_txt.text,
            destination=self.decrypt_tab.dst_txt.text,
            key_pair_name=self.decrypt_tab.spinner.text,
            password=self.decrypt_tab.pw_txt.text,
        )

    def generate(self, _instance):
        """Creates a new asymmetric key pair using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """

        # Validate that the password and its confirmation match
        pw = self.generate_tab.pass_txt.text
        if pw and pw != self.generate_tab.conf_txt.text:
            self.launch_popup(
                "Warning", "Password entries do not match", error=True
            )
            return

        self.init_gui_thread(
            generate_asymmetric_key_pair,
            ["key_pair_name"],
            "Failed to generate asymmetric keys",
            "Generating asymmetric key pair",
            clean="",
            key_pair_name=self.generate_tab.name_txt.text,
            hint=self.generate_tab.hint_txt.text,
            password=self.generate_tab.pass_txt.text,
        )

    def db_backup(self, _instance):
        """Takes a database backup using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            db_backup_wrapper,
            ["key_pair_name", "destination"],
            "Failed to backup the database",
            "Backing up the database",
            clean=self.db_backup_tab.dst_txt.text,
            destination=self.db_backup_tab.dst_txt.text,
            key_pair_name=self.db_backup_tab.spinner.text,
        )

    def db_restore(self, _instance):
        """Restores the database from a backup using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            db_restore_wrapper,
            ["source", "password"],
            "Failed to restore the database",
            "Restoring the database",
            clean=DB_PATH,
            source=self.db_restore_tab.src_txt.text,
            password=self.db_restore_tab.pw_txt.text,
        )

    def import_key(self, _instance):
        """Imports a new key pair using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            import_key_pair,
            ["key_pair_name", "private_key", "public_key"],
            "Failed to import key pair",
            "Importing Key Pair",
            clean="",
            key_pair_name=self.import_tab.name_txt.text,
            private_key=self.import_tab.pri_txt.text,
            public_key=self.import_tab.pub_txt.text,
            hint=self.import_tab.hint_txt.text,
            password=self.import_tab.pass_txt.text,
        )

    def export_key(self, _instance):
        """Exports a single key pair using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            write_key_pair,
            ["key_pair_name", "destination"],
            "Failed to export key pair",
            "Exporting Key Pair",
            clean="",
            key_pair_name=self.export_tab.spinner.text,
            destination=self.export_tab.dst_txt.text,
        )

    def export_all_keys(self, _instance):
        """Exports all key pairs using a separate thread.

        Args:
            _instance (Widget): The Kivy widget that triggered this method.
        """
        self.init_gui_thread(
            write_all_key_pairs,
            ["destination"],
            "Failed to export all key pairs",
            "Exporting All Key Pairs",
            clean="",
            destination=self.export_all_tab.dst_txt.text,
        )

    def build(self):
        """Builds the GUI's overall window layout.

        Returns:
            BoxLayout: The overall layout for the GUI application.
        """

        #: Overall window layout
        root = BoxLayout(orientation="vertical")

        # Action bar
        action_bar = ActionBar()
        action_bar.pos_hint = {"top": 1}
        action_view = ActionView()
        action_previous = ActionPrevious(with_previous=False)
        action_previous.title = self.title
        action_view.add_widget(action_previous)
        keys_btn = ActionButton(text="Keys")
        arch_btn = ActionButton(text="Archives")
        help_btn = ActionButton(text="Help")

        # Action bar button bindings
        keys_btn.bind(on_press=key_pairs_cb)
        arch_btn.bind(on_press=archives_cb)
        help_btn.bind(on_press=help_cb)

        # Attach buttons to action bar's action view
        action_view.add_widget(keys_btn)
        action_view.add_widget(arch_btn)
        action_view.add_widget(help_btn)

        # Attach action view to action bar
        action_bar.add_widget(action_view)

        # The window's tab panel
        tabs = TabbedPanel(do_default_tab=False)
        tabs.tab_width = "95dp"
        tabs.add_widget(self.encrypt_tab)
        tabs.add_widget(self.decrypt_tab)
        tabs.add_widget(self.generate_tab)
        tabs.add_widget(self.db_backup_tab)
        tabs.add_widget(self.db_restore_tab)
        tabs.add_widget(self.import_tab)
        tabs.add_widget(self.export_tab)
        tabs.add_widget(self.export_all_tab)

        # Add action bar and tabs to root layout
        root.add_widget(action_bar)
        root.add_widget(tabs)

        from kivy.core.window import Window
        from gui.callback import win_resize_cb
        from functools import partial

        # Window.bind(on_resize=win_resize_cb)
        Window.bind(on_resize=partial(win_resize_cb, self))

        return root

    def init_gui_thread(self, func, keys, err_msg, msg, clean, **kwargs):
        """Initialize a thread to perform asynchronous processing.

        The thread will run a given function asynchronously to prevent the main
        GUI thread from blocking. Further thread based operations are not
        allowed as the submit buttons are temporarily disabled.

        Args:
            func (function): The function to run on a separate thread.
            keys (List[str]): The names of the kwargs which are required.
            err_msg (str): An error message in case on any exceptions.
            msg (str): A general message to present to the user.
            clean (str): Temporary directory to be removed.
            kwargs (str): All of the functions arguments as keyword arguments.
        """

        # Extract and validate the required args from the keyword args
        required = {kwarg: kwargs[kwarg] for kwarg in kwargs if kwarg in keys}
        valid = validate_required(**required)

        if valid.success:

            # Disable submit buttons temporarily
            self.disable_submits()

            # Launch the thread
            args = (self, func, err_msg, clean)
            Thread(target=gui_thread, args=args, kwargs=kwargs).start()
        else:
            self.launch_popup("Error", valid.msg, error=True)
            return

        self.launch_popup("Info", msg)

    def launch_popup(self, title, msg, error=False):
        """Launches a popup message.

        The message can either be informative or an error. The error message
        popup will take precedence and the info message will be dismissed.

        Args:
            title (str): The title of the popup message.
            msg (str): The content for the popup message.
            error (bool): True if the popup is for an error, defaults to False.
        """

        # Initialize the message as a reST document
        rst = RstDocument(
            text=INFO_TXT.format(title=title, msg=msg),
            scroll_type=["bars", "content"],
            bar_width="12dp",
        )

        # Set the layout for the popup including a close button
        main_layout = BoxLayout(orientation="vertical")
        sub_layout = BoxLayout(orientation="horizontal")
        sub_layout.size_hint_y = None
        sub_layout.height = "40dp"
        button = Button(text="Close")
        sub_layout.add_widget(button)
        main_layout.add_widget(rst)
        main_layout.add_widget(sub_layout)

        # Handle error messages and informative messages separately
        if error:
            button.bind(on_release=self.popup_err.dismiss)
            self.popup_err.clear_widgets()
            self.popup_err.add_widget(main_layout)
            self.popup_err.open()
        else:
            button.bind(on_release=self.popup_msg.dismiss)
            self.popup_msg.clear_widgets()
            self.popup_msg.add_widget(main_layout)
            self.popup_msg.open()

    def disable_submits(self):
        """Disables submit buttons when threaded processing begins."""
        self.encrypt_tab.sub_btn.disabled = True
        self.decrypt_tab.sub_btn.disabled = True
        self.generate_tab.sub_btn.disabled = True
        self.db_backup_tab.sub_btn.disabled = True
        self.db_restore_tab.sub_btn.disabled = True
        self.import_tab.sub_btn.disabled = True
        self.export_tab.sub_btn.disabled = True
        self.export_all_tab.sub_btn.disabled = True

    def enable_submits(self):
        """Enables submit buttons when threaded processing terminates."""
        self.encrypt_tab.sub_btn.disabled = False
        self.decrypt_tab.sub_btn.disabled = False
        self.generate_tab.sub_btn.disabled = False
        self.db_backup_tab.sub_btn.disabled = False
        self.db_restore_tab.sub_btn.disabled = False
        self.import_tab.sub_btn.disabled = False
        self.export_tab.sub_btn.disabled = False
        self.export_all_tab.sub_btn.disabled = False

    def update_drop_downs(self):
        """Syncs the GUI's drop down menus with the latest key name values."""
        self.key_names = get_key_names()
        self.encrypt_tab.spinner.values = self.key_names
        self.decrypt_tab.spinner.values = self.key_names
        self.db_backup_tab.spinner.values = self.key_names
        self.export_tab.spinner.values = self.key_names
