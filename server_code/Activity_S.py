import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import pandas as pd
import plotly.express as px 
import numpy as np
import math

################################################ ACTIVITY ###################################################
@anvil.server.callable
def add_activity(**kwargs):
  Duration = (kwargs["Finish"] - kwargs["Start"]).days
  app_tables.json_table.add_row(Task=kwargs["Task"],
                                Description=kwargs["Description"],
                                Start=kwargs["Start"],
                                Finish=kwargs["Finish"],
                                Duration=Duration,
                                Resource=kwargs["Resource"],
                                Adj=kwargs["Adj"],
                                Group=kwargs["Group"],
                                CP_flag=kwargs["CP_flag"]
                               )
  app_tables.json_table.search(tables.order_by("Start", ascending=False))
  
@anvil.server.callable
def edit_activity(table_entry, **kwargs):
  Duration = (kwargs["Start"] - kwargs["Finish"]).days
  table_entry.update(Task=kwargs["Task"],
                     Description=kwargs["Description"],
                     Start=kwargs["Start"],
                     Finish=kwargs["Finish"],
                     Duration=Duration,
                     Resource=kwargs["Resource"],
                     Adj=kwargs["Adj"],
                     Group=kwargs["Group"],
                     CP_flag=kwargs["CP_flag"]
                    )
  app_tables.json_table.search(tables.order_by("Start", ascending=False))

@anvil.server.callable
def delete_activity(table_entry):
  table_entry.delete()

############################################ END ACTIVITY ###################################################