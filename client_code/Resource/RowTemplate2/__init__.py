from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..EditResource import EditResource

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def edit_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    editing_form = EditResource(item=self.item)
    alert(content=editing_form, large=True)
    self.refresh_data_bindings()

  def delete_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    anvil.server.call('delete_resource', self.item)    
    self.remove_from_parent()
    


    
