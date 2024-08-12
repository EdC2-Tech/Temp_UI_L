import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.email
import anvil.server
from datetime import datetime

@anvil.server.callable
def get_resource():
  return app_tables.resource_table.search()
'''[(row["resource_value"]) for row in app_tables.resource.search()]'''

@anvil.server.callable
def add_resource():
  pass

@anvil.server.callable
def edit_resource():
  pass

@anvil.server.callable
def delete_resource(table_entry):
  table_entry.delete()