import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

################################################### MAIN ###################################################
@anvil.server.callable
def get_all_tables():
  resource_table = app_tables.resource_table.search()
  activity_table = app_tables.activity_table.search()
  json_table = app_tables.json_table.search(tables.order_by("Start"))
  increment  = app_tables.increment.search()
  group_table = app_tables.group_table.search()
  return resource_table, activity_table, json_table, increment, group_table

################################################ END MAIN ###################################################

