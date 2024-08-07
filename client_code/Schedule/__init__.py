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

  def start_datePicker_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass

  def end_datePicker_change(self, **event_args):
    """This method is called when the selected date changes"""
    pass
    
  def import_button_change(self, file, **event_args):
    # Load JSON file and create associated table from data
    anvil.server.call("load_json", file)
    fig = anvil.server.call("draw_chart")
    self.plot_1.figure = fig

  def refresh_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    fig = anvil.server.call("draw_chart")
    self.plot_1.figure = fig

  def __refresh__(self):
    pass

  


    

