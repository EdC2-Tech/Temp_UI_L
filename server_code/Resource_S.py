import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

################################################ RESOURCE ###################################################
@anvil.server.callable
def add_resource(name, description):
  app_tables.resource_table.add_row(resource_name=name,
                                    resource_description=description)

@anvil.server.callable
def edit_resource(table_entry, name, description):
  table_entry.update(resource_name=name,
                     resource_description=description)

@anvil.server.callable
def delete_resource(table_entry):
  table_entry.delete()
  
############################################ END RESOURCE ###################################################