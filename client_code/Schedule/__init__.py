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

    self.interval_drop_down.items = [(row["increment_value"]) for row in get_open_form().increment]
    self.interval_drop_down.selected_value = self.interval_drop_down.items[0]

    self.__refresh_self__()
    
    if not (get_open_form().fig == None):
      self.plot_1.figure = get_open_form().fig
      
  def import_button_change(self, file, **event_args):
    # Load JSON file and create associated table from data
    success = anvil.server.call("load_json", file)
    self.raise_event('x-refresh-tables')
    self.__refresh_self__()
    if success:
      self.__refreshPlot__()
    else:
      anvil.alert("Import unsuccessful, file type unsupported. Gantt chart data must be JSON formatted file.")

  def refresh_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.__refreshPlot__()

  def __refreshPlot__(self):
    if self.CP_flag:
      pass

    if self.group_dropdown.selected_value == None:
      grouping = "All"
    else:
      grouping = self.group_dropdown.selected_value
      
    if self.simplified_flag.checked:
      fig = anvil.server.call("draw_simplified_chart", 
                              start_date=self.start_datePicker.date, 
                              end_date=self.end_datePicker.date, 
                              interval=self.interval_drop_down.selected_value,
                              showCrit=self.CP_flag.checked,
                              Group = grouping
                             )
    else:
      fig = anvil.server.call("draw_full_chart", 
                              start_date=self.start_datePicker.date, 
                              end_date=self.end_datePicker.date, 
                              interval=self.interval_drop_down.selected_value,
                              showCrit=self.CP_flag.checked,
                              Group = grouping
                             )

    get_open_form().fig = fig
    self.plot_1.figure = fig

  def __refresh_self__(self):
    self.group_dropdown.items = [(row["group_name"]) for row in get_open_form().group_table]

  


    

