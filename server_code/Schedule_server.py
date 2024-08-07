import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

import json
import pandas as pd

# Backend for Schedule

@anvil.server.callable
def file_loader(file):
    return anvil.media.from_file(file, 'text/html')
  
def load_json(file):
   with open(file, 'r') as f:
      data = json.load(f)
      f.close()

   return data

def get_Activities():
  pass   
