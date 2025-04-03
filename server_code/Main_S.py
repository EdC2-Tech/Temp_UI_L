import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

################################################### MAIN ###################################################
@anvil.server.callable
def get_all_tables():
  task = anvil.server.launch_background_task('get_all_tables_BG')
  while task.is_running():
    continue
  
  return task
  
@anvil.server.background_task
def get_all_tables_BG():
  resource_table = app_tables.resource_table.search()
  activity_table = app_tables.activity_table.search()
  json_table = app_tables.json_table.search(tables.order_by("Start"))
  increment  = app_tables.increment.search()
  group_table = app_tables.group_table.search()
  anvil.server.task_state["resource_table"] = resource_table
  anvil.server.task_state["activity_table"] = activity_table
  anvil.server.task_state["json_table"] = json_table
  anvil.server.task_state["increment"] = increment
  anvil.server.task_state["group_table"] = group_table

################################################ END MAIN ###################################################

