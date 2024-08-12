from ._anvil_designer import MainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from ..Home import Home
from ..Schedule import Schedule
from ..Activity import Activity
from ..Resource import Resource
from ..Contact import Contact

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Initiate default homepage panel 
    self.content_panel.clear()
    self.content_panel.add_component(Home(), full_width_row=True)

    # Add LOGOS logo to page
    self.logo_image.source = "_/theme/logo.PNG"
    
  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Home(), full_width_row=True)

  def schedule_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Schedule(), full_width_row=True)

  def resource_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Resource(), full_width_row=True)

  def activity_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Activity(), full_width_row=True)

  def contact_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Contact(), full_width_row=True)



  


    

  







