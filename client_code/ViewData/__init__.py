from ._anvil_designer import ViewDataTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ViewData(ViewDataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    """Initialize drop box increment items"""
    item_list = []
    for row in app_tables.increment.search():
      item_list.append((row["increment_value"]))

    self.increment_dropBox.items = item_list
    # Any code you write here will run before the form opens.

  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Main')

  def viewSch_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.refresh_data_bindings()

  def increment_dropBox_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

