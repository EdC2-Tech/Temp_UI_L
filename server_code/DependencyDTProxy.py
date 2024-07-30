import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_dependency():
  return app_tables.dependency.search()

@anvil.server.callable
def add_dependency(dependency_value, dependency_description, resource):
  app_tables.dependency.add_row(dependency_value=dependency_value,
                                dependency_description=dependency_description,
                                resource=resource
                               )
  
@anvil.server.callable
def edit_dependency(table_entry, dependency_value, dependency_description, resource):
  table_entry.update(dependency_value=dependency_value,
                     dependency_description=dependency_description,
                     resource=resource
                     )

@anvil.server.callable
def delete_dependency(table_entry):
  table_entry.delete()
