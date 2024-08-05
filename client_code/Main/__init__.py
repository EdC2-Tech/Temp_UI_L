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
from ..UplinkTest import UplinkTest
from ..Gantt_Test import Gantt_Test
from ..Gantt_JS import Gantt_JS

class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Initiate default homepage panel 
    self.content_panel.clear()
    self.content_panel.add_component(Home())

    # Add LOGOS logo to page
    self.logo_image.source = "_/theme/logo.PNG"
    
  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Home())

  def schedule_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Schedule())

  def resource_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Resource())

  def activity_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Activity())

  def contact_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(UplinkTest())

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Gantt_Test())

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Gantt_JS())

  


    

  







