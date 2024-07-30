from ._anvil_designer import ScheduleTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import plotly.graph_objects as go
from datetime import datetime 
import json

class Schedule(ScheduleTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Initialize defaults to UI options
    self.start_datePicker.date = datetime.now()
    self.end_datePicker.date   = datetime.now()
    
  def import_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def start_datePicker_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass

  def end_datePicker_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass
    
  def file_loader_1_change(self, file, **event_args):
    # Parse file to get array
    anvil.server.call("file_loader_1", file)
    # Clear current tables and replace with content

  def refresh_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def __refresh__(self):
    pass

  


    

