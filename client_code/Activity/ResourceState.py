import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Retrieve resources values from datatable Resource and store in a tuple
resources_available = anvil.server.call('get_resource')
