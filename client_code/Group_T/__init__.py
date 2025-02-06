debugger
from ._anvil_designer import Group_TTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
import anvil.server

from ..Tabulator import Tabulator

# remove some modules we don't need
Tabulator.modules.remove("FrozenColumns")

# change some default options
Tabulator.default_options["selectable"] = True

# change the theme
#Tabulator.theme = "midnight"
#Tabulator.theme = "standard"
Tabulator.theme = "simple"
#Tabulator.theme = "modern"
#Tabulator.theme = "bootstrap3"  # this is the default

# Include a row_selection checkbox column
from ..Tabulator import row_selection_column


def error_handler(e):
  if isinstance(e, anvil.js.ExternalError):
    e = e.original_error
  alert(e)


set_default_error_handling(error_handler)


class Group_T(Group_TTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    try:
      self.tabulator_obj.data = anvil.server.call("get_list_data", n=100)
    except anvil.server.AppOfflineError:
      Notification("App is offline", style="danger").show()

    # FORMATTERS and Editors
    # can be Forms
    #from .FavColorCell import FavColorCell as FavColor

    # Or functions that return components or strings or dom nodes
    def delete_link_formatter(cell, **params):
      l = Link(
        icon="fa:trash",
        foreground="indianred",
        spacing_above="none",
        spacing_below="None",
      )
      return l

    self.tabulator_obj.columns = [
      row_selection_column,  # checkbox select column
      {"title": "Group Name", "field": "group", "editor": True},
      #{"title": "Progress", "field": "progress", "formatter": "progress", "sorter": "number",},
      {"title": "Description", "field": "description", "editor": True},
      #{"title": "Rating", "field": "rating", "formatter": "star", "editor": "star"},
      #{"title": "Favourite Color", "field": "col", "editor": FavColor},
      #{"title": "Date Of Birth",
      # "field": "dob",
      # "editor": "date",
      # "sorter": "date",
      # "formatter": "date",
      # "formatter_params": {"format": "%d/%m/%Y"},
      # "editor_params": {"format": "%d/%m/%Y"},
      #},
      #{"title": "Driver", "field": "car", "formatter": "tickCross"},
      {
        "field": "delete",
        "formatter": delete_link_formatter,
        "width": 40,
        "headerSort": False,
      },
    ]

    self.tabulator_obj.options = {
      "selectable": "highlight",
      "pagination_size_selector": [5, 10, 20],
      "css_class": "table-striped",  # add table striped layout
      #             "selectable_persistence": False,
    }

    # Refer to the example sort drop down box for configuration
    self.columns_dropdown.items = [
      # Add items to drop down list for sort object 
      col["field"] for col in self.tabulator_obj.columns[1:-1]
    ]
    self.fields_dropdown.items = [
      # Add items to drop down list for filter object 
      col["field"] for col in self.tabulator_obj.columns[1:-1]
    ]

  def tabulator_obj_row_click(self, row, **event_args):
    """This method is called when a row is clicked"""
    print(f"{event_args['event_name']} with id: {row.get_data()['id']}")

  # sorting example
  def sort_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    col = self.columns_dropdown.selected_value
    asc = self.ascending_dropdown.selected_value
    self.tabulator_obj.set_sort(col, "asc" if asc else "desc")

  def reset_sort_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.tabulator_obj.clear_sort()

  # filtering example
  def filter_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    field = self.fields_dropdown.selected_value
    symbol = self.type_dropdown.selected_value
    value = self.value_box.text
    print(field, symbol, value)

    self.tabulator_obj.set_filter(field, symbol, value)

  def value_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.filter_button_click()

  def reset_filter_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.tabulator_obj.clear_filter()
    self.value_box.text = ""

  # catch edits from a tabulator builtin editor
  def tabulator_obj_cell_edited(self, cell, **event_args):
    """This method is called when a row is edited - returns the row - will edit the data inplace if writeback is set to True"""
    print(f"{cell.get_field()} from row: {cell.get_row().get_index()} edited")
    print(f"previously: {cell.get_old_value()!r} now {cell.get_value()!r}")
    self.tabulator_row_formatter(cell.get_row())

  # cell clicks
  def do_delete(self, data):
    print(f"deleting row with id {data['id']}")
    c = confirm("are you sure you want to delete this row?")
    print(c)
    if c:
      self.tabulator_obj.delete_row(data["id"])

  def tabulator_obj_cell_click(self, cell, **event_args):
    """This method is called when a cell is clicked - event_args include field and row"""
    field = cell.get_field()
    data = cell.get_data()
    if field == "name":
      Notification(data["name"]).show()
    if field == "delete":
      self.do_delete(data)
    print("cell clicked")

  # easily add a row
  def add_row_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    row = anvil.server.call("get_list_data", n=1)[0]
    if self.tabulator_obj.data:
      row["id"] = max(row["id"] for row in self.tabulator_obj.data) + 1
    print("row with id", row["id"], "being added")
    self.tabulator_obj.add_row(row, True)

  # easily delete rows
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = self.tabulator_obj.get_selected_data()
    if not data:
      return

    self.delete_button.enabled = False

    anvil.js.call("loadSpinner", True)
    from time import sleep

    sleep(0.15)
    indices = [row["id"] for row in data]
    self.tabulator_obj.delete_row(indices)
    anvil.js.call("loadSpinner", False)

  def tabulator_obj_page_loaded(self, pageno, **event_args):
    """This method is called when a page is loaded"""
    print("loaded", pageno)

  def set_locale(self, sender, **event_args):
    """This method is called when the link is clicked"""
    self.tabulator_obj.set_locale(sender.tag)
    print(f"setting locale to {sender.tag}")

  def tabulator_obj_row_formatter(self, row, **event_args):
    """This method is called when the row is rendered - manipulate the tabulator row object"""
    cell = row.get_cell("col")
    color = cell.get_value()
    cell.get_element().style.border = f"2px solid {color}"

  def tabulator_obj_row_selected(self, row, **event_args):
    """This method is called when a row is selected"""
    print(row)

  def tabulator_obj_row_selection_changed(self, rows, data, **event_args):
    """This method is called when the row selection changes"""
    print(f"{event_args['event_name']}: {len(rows)} row(s) selected")
    self.delete_button.enabled = len(rows)
