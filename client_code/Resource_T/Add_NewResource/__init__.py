from ._anvil_designer import Add_NewResourceTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Add_NewResource(Add_NewResourceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.resource_group.items = [name["group_name"] for name in app_tables.group_table.search()]

    # Any code you write here will run before the form opens.
