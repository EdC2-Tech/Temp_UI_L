from ._anvil_designer import ResourceTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .AddResource import AddResource

class Resource(ResourceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    self.__update_table__()
    # Any code you write here will run before the form opens.
    
  def __update_table__(self):
    self.repeating_panel_1.items = get_open_form().resource_table

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    adding_form = AddResource(item=self.item)
    result = alert(content=adding_form, large=True, 
                   buttons=[("Accept", True),
                            ("Cancel", False)
                           ])
    if result:
      resDesc = adding_form.resource_description
      resName = adding_form.resource_name              
      app_tables.resource_table.add_row(resource_name==resName.text,
                                        resource_description=resDesc.text)
      self.raise_event('x-refresh-tables')
      self.__update_table__()
    else:
      return
    
    
    
