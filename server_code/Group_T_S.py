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

def add_row(group_row):  
    row = {
        "Group Name": group_row["group_name"],
        "Group Description": group_row["group_description"],
        "Priority": get_group_color()
    }
    return row

@anvil.server.callable
@timeit
def get_grouplist_data():
    data = []
    n = 0
    for item in app_tables.group_table.search():
        row = add_row(item)
        row["ID"] = n
        n += 1
        data.append(row)
    return data

@anvil.server.callable
def get_group_color():
  return random.choice("High Medium Low".split())
  
@anvil.server.callable
def add_group(group_name, group_description):
  app_tables.group_table.add_row(group_name=group_name,
                                 group_description=group_description
                                )

@anvil.server.callable
def delete_group(table_entry):
  try:
    # Fast search and delete. Entry must only appear once in database
    row = app_tables.group_table.get(group_name=table_entry["Group Name"])
    if row:
      row.delete()
    return    
  except Exception:
    # Slow search and deletes first appearance of element
    for iter in app_tables.group_table.search(): 
      if iter["group_name"]==table_entry["Group Name"]:
          iter.delete()
          return