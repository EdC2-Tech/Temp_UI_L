import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def get_activity():
  return app_tables.json_table.search()

@anvil.server.callable
def add_activity(activity_name, activity_description, resource):
  app_tables.json_table.add_row(Task=activity_name,
                                Description=activity_description,
                                Resource=resource
                               )
  
@anvil.server.callable
def edit_activity(table_entry, activity_name, activity_description, resource):
  table_entry.update(Task=activity_name,
                     Description=activity_description,
                     Resource=resource
                    )

@anvil.server.callable
def delete_activity(table_entry):
  table_entry.delete()
