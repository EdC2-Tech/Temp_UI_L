from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..ResourceState import resources_available

class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.drop_down_1.items = resources_available 

  def edit_dependency(self):
    #resource = self.drop_down_1.selected_value
    dependency_value       = self.text_box_4.text
    dependency_description = self.text_box_5.text
    res                    = self.drop_down_1.selected_value
    
    anvil.server.call('edit_dependency',
                      self.item,
                      dependency_value = dependency_value,
                      dependency_description = dependency_description,
                      resource = res)

  def button_3_click(self, **event_args):
    """This method is called when the edit button is clicked"""
    self.data_row_panel_1.visible=False
    self.data_row_panel_2.visible=True

  def button_1_click(self, **event_args):
    """This method is called when the save button is clicked"""
    self.data_row_panel_1.visible=True
    self.data_row_panel_2.visible=False

    self.edit_dependency()
    self.refresh_data_bindings()

  def button_2_click(self, **event_args):
    """This method is called when the delete button is clicked"""
    anvil.server.call('delete_dependency', self.item)
    self.parent.raise_event('x-refresh-dependencies')
    



  



  

  
