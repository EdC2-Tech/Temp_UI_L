from ._anvil_designer import RowTemplate4Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate4(RowTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    panel = anvil.server.call('get_resource')
    self.Task_resource_edit.items =  {(row["resource_name"]) for row in panel}
    #self.Task_dependency_edit.itmes = None
    
  def edit_dependency(self):
    #resource = self.drop_down_1.selected_value
    task_name       = self.Task_name_edit.text
    task_desciption = self.Task_decription_edit.text
    #task_resource   = self.Task_resource_edit.items
    
    anvil.server.call('edit_dependency',
                      self.item,
                      dependency_value = task_name,
                      dependency_description = task_desciption,
                      resource = None)

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
    



  



  

  
