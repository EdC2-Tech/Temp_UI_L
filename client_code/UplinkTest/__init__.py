from ._anvil_designer import UplinkTestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class UplinkTest(UplinkTestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    param = self.text_box_1.text
    name = anvil.server.call('print_test', param)
    self.text_box_2.text = name

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    ret = anvil.server.call('run_raven')
    self.text_area_1.text = ret
