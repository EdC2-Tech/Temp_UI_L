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
    
  def edit_activity(self):    
    #resource = self.drop_down_1.selected_value
    task_name       = self.Task_name_edit.text
    task_desciption = self.Task_decription_edit.text
    task_start      = self.Start_edit.date
    task_end        = self.End_edit.date
    task_resource   = self.Task_resource_edit.selected
    task_adj        = self.Task_dependency_edit.selected

    #fix
    anvil.server.call('edit_activity',
                      self.item,
                      dependency_value = task_name,
                      dependency_description = task_desciption,
                      resource = None)

  def edit_button_click(self, **event_args):
    json_table     = get_open_form().json_table
    resource_table = get_open_form().resource_table
    self.Task_resource_edit.items =  [(row["resource_name"]) for row in resource_table]
    self.Task_dependency_edit.items = [(row["Task"]) for row in json_table]

    self.Task_resource_edit.add_to_token(self.item['Resource'])
    self.Task_dependency_edit.add_to_token(self.item['Adj'])

    """This method is called when the edit button is clicked"""
    self.data_row_panel_1.visible=False
    self.data_row_panel_2.visible=True

  def save_button_click(self, **event_args):
    """This method is called when the save button is clicked"""
    self.data_row_panel_1.visible=True
    self.data_row_panel_2.visible=False

    self.edit_activity()
    self.raise_event('x-refresh-tables')

  def delete_button_click(self, **event_args):
    """This method is called when the delete button is clicked"""
    anvil.server.call('delete_dependency', self.item)
    self.parent.raise_event('x-refresh-tables')
    



  



  

  
