from ._anvil_designer import Gantt_TestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.image

class Gantt_Test(Gantt_TestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    img = anvil.server.call('run_plotly1_uplink')
    width = img.layout.width
    height = img.layout.height
    alert(f"The image is {width} pixels wide and {height} pixels high")
    self.plot_1.figure = img
  

    
    