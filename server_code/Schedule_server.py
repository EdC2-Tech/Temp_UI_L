import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media

import json
import pandas as pd
import plotly.express as px 
import datetime
import numpy as np
import math

# Backend for Schedule
@anvil.server.callable
def draw_simplified_chart(start_date=0, end_date=0, interval="Days"):
    '''
    Draws a Gantt chart using the simplified list of activities.

    Parameters
    ----------
    start_date : date
        Custom start date specified by user.
    end_date : date
        Custom end date specified by user.
    interval : string
        Custom interval specified by user.

    Returns
    -------
    '''
  # Parameter verification
  
  
@anvil.server.callable
def draw_full_chart(start_date=0, end_date=0, interval="Days"):
  # Parameter verification
  
  # Extract data to draw chart from app tables
  all_records = app_tables.json_table.search() 
  dicts       = [{'Task':r['Task'],
                  'Start':r['Start'],
                  'Finish':r['Finish'],
                  'Adj':r['Adj']
                 } for r in all_records] 
  data        = pd.DataFrame.from_dict(dicts)
  
  # Draw Gantt Chart
  fig = px.timeline(data,
                    y=data["Task"],
                    x_start=data["Start"],
                    x_end=data["Finish"]
  )
  
  # Update x-axis and y-axis with correct information
  fig.update_xaxes(showgrid=True)
  fig.update_yaxes(showgrid=True)

  # Change start date for Gantt drawing
  if not isinstance(start_date, datetime.date):
    # Get range for x (start and end date)
    start_date = data["Start"][0]
  else:
    start_date = start_date
    print("Start date", start_date)
    
  #Change start date for Gantt drawing
  if not isinstance(end_date, datetime.date):
    end_date   = data["Finish"].iloc[-1]
  else:
    end_date = end_date
    print("End date", end_date)
    
  numdays    = (end_date - start_date).days
  print(numdays)

  # Get range for y (# of activities)
  tickvals   = np.arange(0, len(data))
    
  fig.update_layout(
    xaxis = dict(tickmode = 'array',
                 tickvals = [start_date + datetime.timedelta(days=x) for x in range(numdays)],
                 ticktext = [start_date + datetime.timedelta(days=x) for x in range(numdays)],
                 range    = [start_date, end_date]
    ),
    yaxis = dict(tickmode = 'array',
                 tickvals = tickvals,
                 ticktext = data['Task'],
                 range  = [tickvals[0]-1/2, tickvals[-1]+1/2],
                 autorange = "reversed"
    )
  )
  # Change width of activities
  fig.update_traces(width=1)

  # Draw arrows between tasks
  fig = draw_task_links(fig, data)
  
  # Convert to correct time scale
  if interval == "Weeks":
    numweeks = math.ceil(numdays/7)
    fig.update_layout(
      xaxis = dict(tickmode = 'array',
                  tickvals = [start_date + datetime.timedelta(weeks=x) for x in range(numweeks)],
                  ticktext = [start_date + datetime.timedelta(weeks=x) for x in range(numweeks)],
                  range    = [start_date, end_date]
      ),
      yaxis = dict(tickmode = 'array',
                  tickvals = tickvals,
                  ticktext = data['Task'],
                  range  = [tickvals[0]-1/2, tickvals[-1]+1/2],
                  autorange = "reversed"
      )
    )      
  elif interval == "Months":
    nummonths = math.ceil(numdays/28)
    fig.update_layout(
      xaxis = dict(tickmode = 'array',
                  tickvals = [start_date + datetime.timedelta(weeks=x*4) for x in range(nummonths)],
                  ticktext = [start_date + datetime.timedelta(weeks=x*4) for x in range(nummonths)],
                  range    = [start_date, end_date]
      ),
      yaxis = dict(tickmode = 'array',
                  tickvals = tickvals,
                  ticktext = data['Task'],
                  range  = [tickvals[0]-1/2, tickvals[-1]+1/2],
                  autorange = "reversed"
      )
    )     

  
  return fig

@anvil.server.callable
def load_json(file):
  # Try to load the file
  f = file.get_bytes().decode('utf-8').replace("'", '"')
  try:
    data = json.loads(f)
    data = pd.DataFrame.from_dict(data)
  except Exception as e:
    return 0
  
  # Remove existing table from anvil
  app_tables.json_table.delete_all_rows()
  
  # Format data correctly
  data["Start"] = pd.to_datetime(data["Start"]).dt.date
  data["Finish"] = pd.to_datetime(data["Finish"]).dt.date
  data["Duration"] = pd.to_numeric(data["Duration"])
  
  for row in data.iterrows():
    tmp = row[1]
    app_tables.json_table.add_row(Task=tmp["Task"],
                                  Start=tmp["Start"],
                                  Finish=tmp["Finish"],
                                  Duration=tmp["Duration"],
                                  Adj=tmp["Adj"],
                                  CP_Flag=False
                                 )
  return 1

def draw_task_links(fig, json_dict):
    '''
    Draw all arrows in the figure.

    Parameters
    ----------
    fig : plotly.figure
        Figure to draw the arrows on.
    json_dict : dict
        Dictionary of activities.

    Returns
    -------
    new_fig : plotly.figure
        New figure with arrows

    '''
    new_fig = fig
    
    # For each activity draw an arrow
    for link in json_dict.iterrows():
        start_act = link[1]
        
        # For each activity linked to current activity
        for endPoint in link[1]["Adj"]:
            ind     = json_dict.index[json_dict["Task"]==endPoint].tolist()
            end_act = json_dict.loc[ind[0]] 
            
            new_fig = draw_arrow_between_jobs_v2(new_fig, start_act, end_act)
    return new_fig

def draw_arrow_between_jobs_v1(fig, first_job_dict, second_job_dict, color="blue", width=2):
    '''
    Draws an arrow between two gantt activities on a plotly chart. Requires timing
    of the activity to determine start and end spots. 

    Arrow starts from end middle of first activity and ends at the top middle of
    the next activity.
    
    Parameters
    ----------
    fig : plotly.figure
        Figure to draw the arrows on.
    first_job_dict : dict
        Dict of the starting arrow event.
        {Task:<string>,
         Start:<datetime>,
         Finish:<datetime>}
    second_job_dict : dict
        Dict of the ending arrow event. Same type as first_job_dict.
    color : string (Optional)
        Color of line. The default is "blue".
    width : int (Optional)
        Line width. The default is 2.
        
    Returns
    -------
    fig : plotly.figure
        New figure with arrow drawn.

    '''
    ## retrieve tick text and tick vals
    job_yaxis_mapping = dict(zip(fig.layout.yaxis.ticktext,fig.layout.yaxis.tickvals))
    jobs_x_delta      = second_job_dict['Finish'] - second_job_dict['Start']
    jobs_y_delta      = job_yaxis_mapping[first_job_dict['Task']] - job_yaxis_mapping[second_job_dict['Task']]
    
    ## horizontal line segment
    fig = draw_line(fig=fig,
                    x0=first_job_dict['Finish'],
                    x1=second_job_dict['Finish'] - jobs_x_delta/2,
                    y0=job_yaxis_mapping[first_job_dict['Task']],
                    y1=job_yaxis_mapping[first_job_dict['Task']],
                    color=color,
                    width=width
    )
    
    ## vertical line segment
    if jobs_y_delta < 0:
        fig = draw_line(fig=fig,
                        x0=second_job_dict['Finish'] - jobs_x_delta/2,
                        x1=second_job_dict['Finish'] - jobs_x_delta/2,
                        y0=job_yaxis_mapping[first_job_dict['Task']],
                        y1=job_yaxis_mapping[second_job_dict['Task']] - 1/2,
                        color=color,
                        width=width
        )
        ## draw an arrow
        fig.add_annotation(
            x=second_job_dict['Finish'] - jobs_x_delta/2,
            y=job_yaxis_mapping[second_job_dict['Task']] - 1/2,
            xref="x",yref="y",
            showarrow=True,
            ax=0,
            ay=-13,
            ayref='pixel',
            arrowwidth=2,
            arrowcolor=color,
            arrowhead=2,
        )
        
    elif jobs_y_delta >= 0:
        fig = draw_line(fig=fig,
                        x0=second_job_dict['Finish'] - jobs_x_delta/2,
                        x1=second_job_dict['Finish'] - jobs_x_delta/2,
                        y0=job_yaxis_mapping[first_job_dict['Task']],
                        y1=job_yaxis_mapping[second_job_dict['Task']] + 1/2,
                        color=color,
                        width=width
        )       

        ## draw an arrow
        fig.add_annotation(
            x=second_job_dict['Finish'] - jobs_x_delta/2,
            y=job_yaxis_mapping[second_job_dict['Task']] + 1/2,
            xref="x",yref="y",
            showarrow=True,
            ax=0,
            ay=13,
            ayref='pixel',
            arrowwidth=2,
            arrowcolor=color,
            arrowhead=2,
        )

    return fig

def draw_arrow_between_jobs_v2(fig, first_job_dict, second_job_dict, color="blue", width=2):
    '''
    Draws an arrow between two gantt activities on a plotly chart. Requires timing
    of the activity to determine start and end spots. 
    
    Arrow starts from middle bottom of first activity and ends at the beginning of
    the next activity.

    Parameters
    ----------
    fig : plotly.figure
        Figure to draw the arrows on.
    first_job_dict : dict
        Dict of the starting arrow event.
        {Task:<string>,
         Start:<datetime>,
         Finish:<datetime>}
    second_job_dict : dict
        Dict of the ending arrow event. Same type as first_job_dict.
    color : string (Optional)
        Color of line. The default is "blue".
    width : int (Optional)
        Line width. The default is 2.
    
    Returns
    -------
    fig : plotly.figure
        New figure with arrow drawn.

    '''
    ## retrieve tick text and tick vals
    job_yaxis_mapping = dict(zip(fig.layout.yaxis.ticktext,fig.layout.yaxis.tickvals))
    jobs_x_delta      = first_job_dict['Finish'] - first_job_dict['Start']
    jobs_y_delta      = job_yaxis_mapping[first_job_dict['Task']] - job_yaxis_mapping[second_job_dict['Task']]

    ## vertical line segment
    if jobs_y_delta < 0:
        fig = draw_line(fig=fig,
                        x0=first_job_dict['Finish'] - jobs_x_delta/2,
                        x1=first_job_dict['Finish'] - jobs_x_delta/2,
                        y0=job_yaxis_mapping[first_job_dict['Task']] + 1/2,
                        y1=job_yaxis_mapping[second_job_dict['Task']],
                        color=color,
                        width=width
        )
    elif jobs_y_delta >= 0:
        fig = draw_line(fig=fig,
                        x0=first_job_dict['Finish'] - jobs_x_delta/2,
                        x1=first_job_dict['Finish'] - jobs_x_delta/2,
                        y0=job_yaxis_mapping[first_job_dict['Task']] - 1/2,
                        y1=job_yaxis_mapping[second_job_dict['Task']],
                        color=color,
                        width=width
        )        

    ## horizontal line segment
    fig = draw_line(fig=fig,
                    x0=first_job_dict['Finish'] - jobs_x_delta/2,
                    x1=second_job_dict['Start'],
                    y0=job_yaxis_mapping[second_job_dict['Task']],
                    y1=job_yaxis_mapping[second_job_dict['Task']],
                    color=color,
                    width=width
    )

    ## draw an arrow
    fig.add_annotation(
        x=second_job_dict['Start'], 
        y=job_yaxis_mapping[second_job_dict['Task']],
        xref="x",yref="y",
        showarrow=True,
        ax=-10,
        ay=0,
        arrowwidth=2,
        arrowcolor=color,
        arrowhead=2,
    )
    return fig

def draw_line(fig, x0, x1, y0, y1, color="blue", width=2):
    '''
    Draws a line between 2 coordinate points.

    Parameters
    ----------
    fig : plotly figure
        Figure to draw line on.
    x0 : object
        Start x coordinate.
    x1 : object
        End x coordinate.
    y0 : object
        Start y coordinate.
    y1 : object
        End y coordinate.
    color : string (Optional)
        Color of line. The default is "blue".
    width : int (Optional)
        Line width. The default is 2.

    Returns
    -------
    fig : plotly figure
        Figure with lines

    '''
    ## horizontal line segment
    fig.add_shape(
        x0=x0, y0=y0, 
        x1=x1, y1=y1,
        line=dict(color=color, width=width)
    )
    
    return fig     
