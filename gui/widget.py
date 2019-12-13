"""Customized extensions of Kivy widgets."""

from functools import partial

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.rst import RstDocument
from kivy.uix.spinner import Spinner
from kivy.uix.splitter import Splitter
from kivy.uix.textinput import TextInput
from kivy.utils import platform

from gui.callback import file_cb


class BrowseButton(Button):
    """Extension of a Kivy Button class used to pick file and directories.

    Selection of the file or directory is performed via a call back function
    that is triggered when the button is pressed.

    Args:
        text_field: Field that is populated with a file or directory.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The display text for the submit button.
        size_hint_x (float): Set to always occupy 25% of the window's width.
        size_hint_y: Set to None to allow for a fixed height.
        height (int): The height of the button.
    """

    def __init__(self, text_field, **kwargs):
        super(BrowseButton, self).__init__(**kwargs)

        self.text = "Browse"
        self.size_hint_x = 0.2
        self.size_hint_y = None
        self.height = "30dp"
        self.bind(on_press=partial(file_cb, text_field))


class DisabledText(TextInput):
    """Extension of a Kivy TextInput that is set to the disabled state.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        multiline (bool): Set to False to disable multiline input.
        disabled (bool): Set to True to stop the user from editing the field.
        size_hint_x (float): Set to always occupy 50% of the window's width.
    """

    def __init__(self, **kwargs):
        super(DisabledText, self).__init__(**kwargs)

        self.multiline = False
        self.disabled = True
        self.size_hint_x = 0.5


class DropDownCustom(DropDown):
    """Extension of a Kivy DropDown used in the SpinnerCustom class.

    Args:
        kwargs: Any additional keyword arguments.
    """

    def __init__(self, **kwargs):
        super(DropDownCustom, self).__init__(**kwargs)

        self.container.spacing = "-3dp"


class FileRow(BoxLayout):
    """Extension of a Kivy BoxLayout with a label, text field, and a button.

    Args:
        text (str): The text that populates the label.
        text_field (DisabledText): Field that is populated with a file or dir.
        kwargs: Any additional keyword arguments.

    Attributes:
        orientation (str): The direction in which widgets are arranged.
        size_hint_y: Set to None to allow for a fixed height.
        height (int): The height of the row.
    """

    def __init__(self, text, text_field, **kwargs):
        super(FileRow, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "32dp"

        self.add_widget(LabelCustom(text=text))
        self.add_widget(text_field)
        self.add_widget(BrowseButton(text_field))


class FreeText(TextInput):
    """Extension of Kivy's TextInput set for free text or password input.

    Args:
        pw (bool): True if the input is for a password, defaults to False.
        kwargs: Any additional keyword arguments.

    Attributes:
        multiline (bool): Set to False to disable multiline input.
        password (bool): True if the field is a password input field.
        size_hint_x (float): Set to always occupy 75% of the window's width.
        write_tab (bool): Set to False to allow tabbing between elements.
    """

    def __init__(self, pw=False, **kwargs):
        super(FreeText, self).__init__(**kwargs)

        self.multiline = False
        self.password = pw
        self.size_hint_x = 0.7
        self.write_tab = False


class FreeTextRow(BoxLayout):
    """Extension of a Kivy BoxLayout with a label and a text field.

    Args:
        text (str): The text that populates the label.
        text_field (DisabledText): Field that is populated with a file or dir.
        kwargs: Any additional keyword arguments.

    Attributes:
        orientation (str): The direction in which widgets are arranged.
        size_hint_y: Set to None to allow for a fixed height.
        height (int): The height of the row.
    """

    def __init__(self, text, text_field, **kwargs):
        super(FreeTextRow, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "32dp"

        self.add_widget(LabelCustom(text=text))
        self.add_widget(text_field)


class LabelCustom(Label):
    """Extension of a Kivy Label with specific alignment and sizing.

    Args:
        text (str): The text that populates the label.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The text that populates the label.
        halign (str): The horizontal alignment of the elements.
        valign (str): The vertical alignment of the elements.
        size_hint_x (float): Set to always occupy 25% of the window's width.
    """

    def __init__(self, text, **kwargs):
        super(LabelCustom, self).__init__(**kwargs)

        self.text = text
        self.halign = "left"
        self.valign = "center"
        self.size_hint_x = 0.3
        self.bind(size=self.setter("text_size"))


class LabelHidden(Label):
    """Extension of a Kivy Label with no text to fill empty space.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): Set to en empty string to make the widget hidden.
        size_hint_x (float): Set to always occupy 75% of the window's width.
    """

    def __init__(self, **kwargs):
        super(LabelHidden, self).__init__(**kwargs)

        self.text = ""
        self.size_hint_x = 0.7


class SpinnerCustom(Spinner):
    """Extension of a Kivy Spinner to select Key Pair names.

    Args:
        key_names (list[str]): Values for the spinner which are key pair names.
        kwargs: Any additional keyword arguments.

    Attributes:
        dropdown_cls (class): The class used for the spinner's dropdown.
        text_autoupdate (bool): Automatically sets the initial value.
        values (list[str]): Values for the spinner which are key pair names.
        valign (str): The vertical alignment of the elements.
        halign (str): The horizontal alignment of the elements.
        padding_x (int): The amount of blank space added in the x direction.
        sync_height (bool): Child elements use the height of the main element.
    """

    def __init__(self, key_names, **kwargs):
        super(SpinnerCustom, self).__init__(**kwargs)

        self.dropdown_cls = DropDownCustom
        self.text_autoupdate = True
        self.values = key_names
        self.valign = "middle"
        self.halign = "center"
        self.padding_x = "5dp"
        self.sync_height = True
        self.size_hint_x = 0.7
        self.bind(size=self.setter("text_size"))


class SpinnerRow(BoxLayout):
    """Extension of a Kivy BoxLayout with a label and spinner.

    Args:
        text (str): The text that populates the label for the spinner.
        spinner (Spinner): Spinner that populates this row.
        kwargs: Any additional keyword arguments.

    Attributes:
        orientation (str): The direction in which widgets are arranged.
        size_hint_y: Set to None to allow for a fixed height.
        height (int): The height of the row.
    """

    def __init__(self, text, spinner, **kwargs):
        super(SpinnerRow, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "32dp"

        self.add_widget(LabelCustom(text=text))
        self.add_widget(spinner)


class SplitterCustom(Splitter):
    """Extension of a Kivy Splitter to split tabs with help information.

    Args:
        rest_doc (str): The text that populates the help information.
        kwargs: Any additional keyword arguments.

    Attributes:
        sizable_from (str): The direction the splitter will expand.
        min_size (int): The minimum size for the splitter section.
        max_size (int): The maximum size for the expanded splitter section.
        size_hint_x: Set to None to allow for a fixed width.
        width (int): The initial width of the splitter section.
        keep_within_parent (bool): Lock the splitter bar in the parent window.
        rescale_with_parent (bool): Tries to scale if with the parent window.
        size_hint_y: Set to None to allow for specific height values
        height (int): Set to match the window's height.
    """

    def __init__(self, rest_doc, **kwargs):
        super(SplitterCustom, self).__init__(**kwargs)

        self.sizable_from = "right"
        self.min_size = "10dp"
        self.size_hint_x = None
        self.width = "10dp"
        self.keep_within_parent = True
        self.rescale_with_parent = True
        self.size_hint_y = None
        self.height = Window.height

        # Handle the splitter's max_size based on the platform
        if platform == "android":
            self.max_size = "225dp"
        else:
            self.max_size = "380dp"

        self.add_widget(RstDocument(text=rest_doc))


class SubmitButton(Button):
    """Extension of a Kivy Button class used to submit forms.

    Args:
        bind_to (function): Function executed when this button is pressed.
        kwargs: Any additional keyword arguments.

    Attributes:
        text (str): The display text for the submit button.
        size_hint_x: Set to always occupy 25% of the window's width.
    """

    def __init__(self, bind_to, **kwargs):
        super(SubmitButton, self).__init__(**kwargs)

        self.text = "Submit"
        self.size_hint_x = 0.3
        self.bind(on_press=bind_to)


class SubmitRow(BoxLayout):
    """Extension of a Kivy BoxLayout with only a submit button.

    Args:
        button (Button): The submit button object to display.
        kwargs: Any additional keyword arguments.

    Attributes:
        orientation (str): The direction in which widgets are arranged.
        size_hint_y: Set to None to allow for a fixed height.
        height (int): The height of the row.
    """

    def __init__(self, button, **kwargs):
        super(SubmitRow, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "30dp"

        self.add_widget(button)
        self.add_widget(LabelHidden())
