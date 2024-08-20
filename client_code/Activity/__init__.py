from ._anvil_designer import ActivityTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Activity(ActivityTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Populate table with existing information
    self.repeating_panel_1.items = get_open_form().json_table

    # Populate edit_resource_multi dropdown menu
    self.edit_resource_multi.items = [(row["resource_name"]) for row in get_open_form().resource_table]

    # Populate edit_activity_multi dropdown menu
    self.edit_dependency_multi.items = [(row["Task"]) for row in get_open_form().json_table]

    # Populate edit_group
    self.edit_group.items = [(row["group_name"]) for row in get_open_form().group_table]

    # Set event handlers
    #self.repeating_panel_1.set_event_handler('x-refresh-dependencies', self.refresh_dependencies)
  
  def refresh_dependencies(self, **event_args):
    self.raise_event('x-refresh-tables')
    self.repeating_panel_1.items = get_open_form().json_table 
    pass
  
  def pg_size_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    rowPerPage = int(self.pg_size.text) + 2
    if rowPerPage > 50:
      rowPerPage = 50
      
    self.data_grid_1.rows_per_page = rowPerPage

  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    activity_name        = self.edit_dep_val.text
    activity_description = self.edit_dep_des.text
    activity_resource    = self.edit_resource_multi.items
    activity_dependency  = self.edit_dependency_multi.items 
    activity_CP_flag     = self.critical_checkbox.checked
    
    anvil.server.call('add_activity',
                      Task = activity_name,
                      Description = activity_description,
                      Resource = activity_resource,
                      Adj = activity_dependency,
                      CP_flag = activity_CP_flag,
                      
                     )
    # refresh grid panel
    self.refresh_dependencies()
    
    # clear after adding new row
    self.edit_dep_val.text = ''
    self.edit_dep_des.text = ''
