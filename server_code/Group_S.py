import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

################################################ GROUP ######################################################
  
@anvil.server.callable
def edit_group(table_entry, group_name, group_description):
  table_entry.update(group_name=group_name,
                     group_description = group_description
                    )

############################################### END GROUP ###################################################