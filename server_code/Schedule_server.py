import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import json
import pandas as pd

# Backend for Schedule

@anvil.server.callable
def file_loader_1(file):
    # Parse file to get array
    data = pd.DataFrame.from_dict(load_json(file))

    # Convert time to datetime object
    data["Start"] = pd.to_datetime(data["Start"])
    data["Finish"] = pd.to_datetime(data["Finish"])
  
    # Clear current tables and replace with content
    app_tables.Activity_table.delete_all_rows()
    for i in data.iterrows():
      item = i[1]
      app_tables.Activity_table.add_rows(item)
  
    #
  
def load_json(file):
   with open(file, 'r') as f:
      data = json.load(f)
      f.close()

   return data

def get_Activities():
  pass   
