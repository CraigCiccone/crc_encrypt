"""GUI Table related functions and classes."""

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView

from utils.helpers import get_archives, get_key_pairs, get_table_width

# Global values for the width of tables. Set globally to avoid recalculation
ARCH_MAX_WIDTH = 0
KEYS_MAX_WIDTH = 0


class ArchiveRecycleView(RecycleView):
    """Extension of Kivy's RecycleView to present Archive meta data.

    A RecycleView is used as it allows the table data to be handled more
    efficiently by Kivy.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        viewclass (str): The class that sets the content for this view.
        scroll_type (list[str]): The ways the widget can be scrolled.
        bar_width (int): The width of the displayed scroll bar.
        do_scroll_x (bool): Set to True to allow horizontal scrolling.
        do_scroll_y (bool): Set to True to allow vertical scrolling.
        size_hint (tuple[int, int]): Set to fill the parent viewport.
    """

    def __init__(self, **kwargs):
        super(ArchiveRecycleView, self).__init__(**kwargs)

        # Set the RecycleView's widgets and parameters
        self.add_widget(TableRecycleBoxLayout())
        self.viewclass = "ArchiveTableRow"
        self.scroll_type = ["bars", "content"]
        self.bar_width = "12dp"
        self.do_scroll_x = True
        self.do_scroll_y = True
        # self.size_hint = (1, 1)

        # Set the data for the RecycleView with a bold faced header row
        tmp_data = [
            {
                "name": "[b]Name[/b]",
                "src_path": "[b]Source[/b]",
                "dst_path": "[b]Destination[/b]",
                "kp": "[b]Key Pair Name[/b]",
                "timestamp": "[b]Timestamp[/b]",
            }
        ]
        tmp_data += get_archives()
        self.data = tmp_data

        # Set the max width for the Archive table data
        set_max_width(tmp_data)


class ArchiveTableRow(BoxLayout):
    """Represents a single row of Archive meta data using Kivy's BoxLayout.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        orientation (str): The direction in which widgets are arranged.
        size_hint: Set to None to force the desired sizing.
        width (int): The overall width of the row.
        height (int): The overall height of the row.
    """

    def __init__(self, **kwargs):
        super(ArchiveTableRow, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.width = ARCH_MAX_WIDTH
        self.height = "32dp"

        self.name_lbl = Label(markup=True, text="")
        self.src_path_lbl = Label(markup=True, text="")
        self.dst_path_lbl = Label(markup=True, text="")
        self.kp_lbl = Label(markup=True, text="")
        self.timestamp_lbl = Label(markup=True, text="")

        self.add_widget(self.name_lbl)
        self.add_widget(self.src_path_lbl)
        self.add_widget(self.dst_path_lbl)
        self.add_widget(self.kp_lbl)
        self.add_widget(self.timestamp_lbl)

    def on_parent(self, _screen, _parent):
        """Updates the row values when parent events are fired.

        Args:
            _screen (Widget): Required for Kivy on_parent.
            _parent (Widget): Required for Kivy on_parent.
        """
        self.name_lbl.text = self.name
        self.src_path_lbl.text = self.src_path
        self.dst_path_lbl.text = self.dst_path
        self.kp_lbl.text = self.kp
        self.timestamp_lbl.text = self.timestamp


class KeysRecycleView(RecycleView):
    """Extension of Kivy's RecycleView to present Key Pair meta data.

    A RecycleView is used as it allows the table data to be handled more
    efficiently by Kivy.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        viewclass (str): The class that sets the content for this view.
        scroll_type (list[str]): The ways the widget can be scrolled.
        bar_width (int): The width of the displayed scroll bar.
        do_scroll_x (bool): Set to True to allow horizontal scrolling.
        do_scroll_y (bool): Set to True to allow vertical scrolling.
        size_hint (tuple[int, int]): Set to fill the parent viewport.
    """

    def __init__(self, **kwargs):
        super(KeysRecycleView, self).__init__(**kwargs)

        # Set the RecycleView's widgets and parameters
        self.add_widget(TableRecycleBoxLayout())
        self.viewclass = "KeysTableRow"
        self.scroll_type = ["bars", "content"]
        self.bar_width = "12dp"
        self.do_scroll_x = True
        self.do_scroll_y = True
        # self.size_hint = (1, 1)

        # Set the data for the RecycleView with a bold faced header row
        tmp_data = [
            {
                "name": "[b]Name[/b]",
                "pw": "[b]Has Password[/b]",
                "hint": "[b]Password Hint[/b]",
                "strong": "[b]Strong Password[/b]",
                "timestamp": "[b]Timestamp[/b]",
            }
        ]
        tmp_data += get_key_pairs()
        self.data = tmp_data

        # Set the max width for the Key Pairs table data
        set_max_width(tmp_data, keys=True)


class KeysTableRow(BoxLayout):
    """Represents a single row of Key Pair meta data using Kivy's BoxLayout.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        orientation (str): The direction in which widgets are arranged.
        size_hint: Set to None to force the desired sizing.
        width (int): The overall width of the row.
        height (int): The overall height of the row.
    """

    def __init__(self, **kwargs):
        super(KeysTableRow, self).__init__(**kwargs)

        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.width = KEYS_MAX_WIDTH
        self.height = "32dp"

        self.name_lbl = Label(markup=True, text="")
        self.pw_lbl = Label(markup=True, text="")
        self.hint_lbl = Label(markup=True, text="")
        self.strong_lbl = Label(markup=True, text="")
        self.timestamp_lbl = Label(markup=True, text="")

        self.add_widget(self.name_lbl)
        self.add_widget(self.pw_lbl)
        self.add_widget(self.hint_lbl)
        self.add_widget(self.strong_lbl)
        self.add_widget(self.timestamp_lbl)

    def on_parent(self, _screen, _parent):
        """Updates the row values when parent events are fired.

        Args:
            _screen (Widget): Required for Kivy on_parent.
            _parent (Widget): Required for Kivy on_parent.
        """
        self.name_lbl.text = self.name
        self.pw_lbl.text = self.pw
        self.hint_lbl.text = self.hint
        self.strong_lbl.text = self.strong
        self.timestamp_lbl.text = self.timestamp


class TableRecycleBoxLayout(RecycleBoxLayout):
    """Layout used for tables implemented using Kivy's RecycleBoxLayout.

    Args:
        kwargs: Any additional keyword arguments.

    Attributes:
        default_size: Set to None to force the desired sizing.
        default_size_hint: Set to None to force the desired sizing.
        size_hint_y: Set to None to force the desired sizing.
        size_hint_x: Set to None to force the desired sizing.
        orientation (str): The direction in which widgets are arranged.
    """

    def __init__(self, **kwargs):
        super(TableRecycleBoxLayout, self).__init__(**kwargs)

        self.default_size = (None, None)
        self.default_size_hint = (None, None)
        self.size_hint_y = None
        self.size_hint_x = None
        self.orientation = "vertical"

        # Force the height and width to be equal to the minimum height and
        # width. Equivalent to kv language of: height: self.minimum_height
        self.bind(minimum_height=self._min_height)
        self.bind(minimum_width=self._min_width)

    def _min_height(self, _instance, value):
        """Method to set the height equal to the minimum height.

        Args:
            _instance (Widget): Required parameter for Kivy.
            value (int): The new value for the height.
        """
        self.height = value

    def _min_width(self, _instance, value):
        """Method to set the width equal to the minimum width.

        Args:
            _instance (Widget): Required parameter for Kivy.
            value (int): The new value for the width.
        """
        self.width = value


def set_max_width(data, keys=False):
    """Sets the max width of tables displayed using Kivy's RecycleView.

    The max width parameters are stored as global variables to prevent having
    to set them for each and every row. Instead, they are set once when the
    RecycleView is instantiated.

    Args:
        data (list[dict[str, str]]): The table's data elements.
        keys (bool): True if key table max width is set, defaults to False.
    """
    if keys:
        global KEYS_MAX_WIDTH
        KEYS_MAX_WIDTH = get_table_width(data)
    else:
        global ARCH_MAX_WIDTH
        ARCH_MAX_WIDTH = get_table_width(data)
