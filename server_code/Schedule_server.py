import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

import json
import pandas as pd
import cloudpickle
from urllib.request import urlopen

# Backend for Schedule
@anvil.server.callable
def get_chart_obj():
  chart = app_tables.chart_obj.get(name='chart')['chart']
  chart = cloudpickle.load(urlopen(chart.url)) 
  
  return chart
  
def load_json(file):
   with open(file, 'r') as f:
      data = json.load(f)
      f.close()

   return data

def get_Activities():
  pass   
