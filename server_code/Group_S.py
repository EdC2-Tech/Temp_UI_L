import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

################################################ GROUP ######################################################
@anvil.server.callable
def add_group(group_name, group_description):
  app_tables.group_table.add_row(group_name=group_name,
                                 group_description=group_description
                               )
  
@anvil.server.callable
def edit_group(table_entry, group_name, group_description):
  table_entry.update(group_name=group_name,
                     group_description = group_description
                    )

@anvil.server.callable
def delete_group(table_entry):
  table_entry.delete()

############################################### END GROUP ###################################################