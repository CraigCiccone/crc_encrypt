"""
Customized extensions of Kivy tabs. Note that each tab's main layout consists
of the tab content and a horizontally split help section. The help section is
populated using GUI function docstrings.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanelItem

import gui.app
from config import (
    DB_BACKUP_HELP,
    DB_RESTORE_HELP,
    DECRYPT_HELP,
    ENCRYPT_HELP,
    EXPORT_ALL_HELP,
    EXPORT_HELP,
    GENERATE_HELP,
    IMPORT_HELP,
)
from gui.widget import (
    DisabledText,
    FileRow,
    FreeText,
    FreeTextRow,
    SpinnerCustom,
    SpinnerRow,
    SplitterCustom,
    SubmitButton,
    SubmitRow,
)


class DatabaseBackupTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to backup the database.

    Args:
        key_names (list[str]): All the key pair names available in the spinner.
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        spinner (SpinnerCustom): Selection of key pairs available.
        dst_txt (DisabledText): The destination picked by the user.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, key_names, func, **kwargs):
        super(DatabaseBackupTab, self).__init__(**kwargs)

        self.text = "DB Backup"
        self.spinner = SpinnerCustom(key_names)
        self.dst_txt = DisabledText()
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=4, padding="15dp", spacing="25dp")

        name_row = SpinnerRow("*Key Pair Name", self.spinner)
        dst_row = FileRow("*Destination", self.dst_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(name_row)
        tab_layout.add_widget(dst_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(DB_BACKUP_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class DatabaseRestoreTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to restore the DB from a backup.

    Args:
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        src_text (DisabledText): The source picked by the user.
        pw_txt (FreeText): The password provided by the user.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, func, **kwargs):
        super(DatabaseRestoreTab, self).__init__(**kwargs)

        self.text = "DB Restore"
        self.src_txt = DisabledText()
        self.pw_txt = FreeText(pw=True)
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=4, padding="15dp", spacing="25dp")

        src_row = FileRow("*Source", self.src_txt)
        pw_row = FreeTextRow("*Password", self.pw_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(src_row)
        tab_layout.add_widget(pw_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(DB_RESTORE_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class DecryptTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to present a form for decryption.

    Args:
        key_names (list[str]): All the key pair names available in the spinner.
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        spinner (SpinnerCustom): Selection of key pairs available.
        src_text (DisabledText): The source picked by the user.
        dst_text (DisabledText): The destination picked by the user.
        pw_txt (FreeText): The password provided by the user.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, key_names, func, **kwargs):
        super(DecryptTab, self).__init__(**kwargs)

        self.text = "Decrypt"
        self.spinner = SpinnerCustom(key_names)
        self.src_txt = DisabledText()
        self.dst_txt = DisabledText()
        self.pw_txt = FreeText(pw=True)
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=6, padding="15dp", spacing="25dp")

        name_row = SpinnerRow("*Key Pair Name", self.spinner)
        src_row = FileRow("*Source", self.src_txt)
        dst_row = FileRow("*Destination", self.dst_txt)
        pw_row = FreeTextRow("Password", self.pw_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(name_row)
        tab_layout.add_widget(src_row)
        tab_layout.add_widget(dst_row)
        tab_layout.add_widget(pw_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(DECRYPT_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class EncryptTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to present a form for encryption.

    Args:
        key_names (list[str]): All the key pair names available in the spinner.
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        src_text (DisabledText): The source picked by the user.
        dst_text (DisabledText): The destination picked by the user.
        spinner (SpinnerCustom): Selection of key pairs available.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, key_names, func, **kwargs):
        super(EncryptTab, self).__init__(**kwargs)

        self.text = "Encrypt"
        self.src_txt = DisabledText()
        self.dst_txt = DisabledText()
        self.spinner = SpinnerCustom(key_names)
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=5, padding="15dp", spacing="25dp")

        name_row = SpinnerRow("*Key Pair Name", self.spinner)
        src_row = FileRow("*Source", self.src_txt)
        dst_row = FileRow("*Destination", self.dst_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(name_row)
        tab_layout.add_widget(src_row)
        tab_layout.add_widget(dst_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(ENCRYPT_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class ExportAllTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to export all key pairs.

    Args:
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        dst_text (DisabledText): The destination picked by the user.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, func, **kwargs):
        super(ExportAllTab, self).__init__(**kwargs)

        self.text = "Export All"
        self.dst_txt = DisabledText()
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=3, padding="15dp", spacing="25dp")

        dst_row = FileRow("*Destination", self.dst_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(dst_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(EXPORT_ALL_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class ExportTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to present a form to export keys.

    Args:
        key_names (list[str]): All the key pair names available in the spinner.
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        spinner (SpinnerCustom): Selection of key pairs available.
        dst_text (DisabledText): The destination picked by the user.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, key_names, func, **kwargs):
        super(ExportTab, self).__init__(**kwargs)

        self.text = "Export"
        self.spinner = SpinnerCustom(key_names)
        self.dst_txt = DisabledText()
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=4, padding="15dp", spacing="25dp")

        name_row = SpinnerRow("*Key Pair Name", self.spinner)
        dst_row = FileRow("*Destination", self.dst_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(name_row)
        tab_layout.add_widget(dst_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(EXPORT_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class GenerateTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to facilitate generating keys.

    Args:
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        name_txt (FreeText): The name of the key pair provided by the user.
        hint_txt (FreeText): An optional password hint provided by the user.
        pass_txt (FreeText): The password provided by the user.
        conf_txt (FreeText): The password provided by the user as confirmation.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, func, **kwargs):
        super(GenerateTab, self).__init__(**kwargs)

        self.text = "Generate"
        self.name_txt = FreeText()
        self.hint_txt = FreeText()
        self.pass_txt = FreeText(pw=True)
        self.conf_txt = FreeText(pw=True)
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=6, padding="15dp", spacing="25dp")

        name_row = FreeTextRow("*Key Pair Name", self.name_txt)
        hint_row = FreeTextRow("Password Hint", self.hint_txt)
        pw_row = FreeTextRow("Password", self.pass_txt)
        conf_row = FreeTextRow("Confirm Password", self.conf_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(name_row)
        tab_layout.add_widget(hint_row)
        tab_layout.add_widget(pw_row)
        tab_layout.add_widget(conf_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(GENERATE_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)


class ImportTab(TabbedPanelItem):
    """Extension of a Kivy TabbedPanelItem to present a form to import keys.

    Args:
        func (function): Triggered when the submit button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The title of the tab.
        name_txt (FreeText): The name of the key pair provided by the user.
        pri_text (DisabledText): The private key location picked by the user.
        pub_text (DisabledText): The public key location picked by the user.
        hint_txt (FreeText): An optional password hint provided by the user.
        pass_txt (FreeText): The password provided by the user.
        sub_btn (SubmitButton): The submit button for this tab.
    """

    def __init__(self, func, **kwargs):
        super(ImportTab, self).__init__(**kwargs)

        self.text = "Import"
        self.name_txt = FreeText()
        self.pri_txt = DisabledText()
        self.pub_txt = DisabledText()
        self.hint_txt = FreeText()
        self.pass_txt = FreeText(pw=True)
        self.sub_btn = SubmitButton(func)

        scroll_layout = ScrollView(scroll_type=["bars"], bar_width="12dp")
        main_layout = GridLayout(cols=2, size_hint_y=None, height="340dp")
        tab_layout = GridLayout(rows=7, padding="15dp", spacing="25dp")

        name_row = FreeTextRow("*Key Pair Name", self.name_txt)
        pri_row = FileRow("*Private Key", self.pri_txt)
        pub_row = FileRow("*Public Key", self.pub_txt)
        hint_row = FreeTextRow("Password Hint", self.hint_txt)
        pw_row = FreeTextRow("Password", self.pass_txt)
        sub_row = SubmitRow(self.sub_btn)
        fil_row = BoxLayout(orientation="horizontal")
        tab_layout.add_widget(name_row)
        tab_layout.add_widget(pri_row)
        tab_layout.add_widget(pub_row)
        tab_layout.add_widget(hint_row)
        tab_layout.add_widget(pw_row)
        tab_layout.add_widget(sub_row)
        tab_layout.add_widget(fil_row)

        self.splitter = SplitterCustom(IMPORT_HELP)
        main_layout.add_widget(self.splitter)
        main_layout.add_widget(tab_layout)
        scroll_layout.add_widget(main_layout)
        self.add_widget(scroll_layout)
