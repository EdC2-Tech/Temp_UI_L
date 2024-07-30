from ._anvil_designer import Gantt_JSTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Gantt_JS(Gantt_JSTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    img = anvil.server.call('run_plotly2_uplink')
    width = img.layout.width
    height = img.layout.height
    alert(f"The image is {width} pixels wide and {height} pixels high")
    self.plot_1.figure = img
    
