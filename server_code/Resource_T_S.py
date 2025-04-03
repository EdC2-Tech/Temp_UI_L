import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import random
from functools import wraps
from time import time

# Call using @timeit similar to @anvil.server.callable
def timeit(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        str_args = ", ".join(str(arg) for arg in args)
        str_kwargs = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        args_kwargs = f"{str_args}, {str_kwargs}" if args and kwargs else f"{str_args}{str_kwargs}"

        print(f"{f.__name__}({args_kwargs}) called")
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        print(f"{f.__name__} took: {te-ts:.4f} sec")
        return result

    return wrap

def add_row(resource_row):  
    row = {
        "Resource Name": resource_row["resource_name"],
        "Resource Description": resource_row["resource_description"],
        "Priority": get_resource_color()
    }
    return row

@anvil.server.callable
@timeit
def get_resourcelist_data():
    data = []
    n = 0
    for item in app_tables.resource_table.search():
        row = add_row(item)
        row["ID"] = n
        n += 1
        data.append(row)
    return data

@anvil.server.callable
def get_resource_color():
  return random.choice("High Medium Low".split())
  
@anvil.server.callable
def add_resource(resource_name, resource_description):
  app_tables.resource_table.add_row(resource_name=resource_name,
                                 resource_description=resource_description
                                )

@anvil.server.callable
def delete_resource(table_entry):
  try:
    # Fast search and delete. Entry must only appear once in database
    row = app_tables.resource_table.get(resource_name=table_entry["Resource Name"])
    if row:
      row.delete()
    return    
  except Exception:
    # Slow search and deletes first appearance of element
    for iter in app_tables.resource_name.search(): 
      if iter["resource_name"]==table_entry["Resource Name"]:
          iter.delete()
          return

