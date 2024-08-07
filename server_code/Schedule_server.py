import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

import json
import pandas as pd
import plotly.express as px 

# Backend for Schedule
@anvil.server.callable
def draw_chart(plot_dest):
  df = px.data.gapminder().query("country == 'Canada'")
  fig = px.bar(df, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
             labels={'pop':'population of Canada'}, height=400)
  return fig

@anvil.server.callable
def load_json(file):
  # Remove existing table from anvil
  app_tables.json_table.delete_all_rows()
  
  # Load file from json
  f = file.get_bytes().decode('utf-8').replace("'", '"')
  data = json.loads(f)
  data = pd.DataFrame.from_dict(data)

  data["Start"] = pd.to_datetime(data["Start"]).dt.date
  data["Finish"] = pd.to_datetime(data["Finish"]).dt.date
  data["Duration"] = pd.to_numeric(data["Duration"])
  
  for row in data.iterrows():
    tmp = row[1]
    app_tables.json_table.add_row(Task=tmp["Task"],
                                  Start=tmp["Start"],
                                  Finish=tmp["Finish"],
                                  Duration=tmp["Duration"],
                                  Adj=tmp["Adj"]
                                 )

  print("Table creation successful")
  return 

def get_Activities():
  pass   
