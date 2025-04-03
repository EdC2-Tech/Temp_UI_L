import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import random
from datetime import datetime, timedelta

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

def random_date(first_date, second_date):
    first_timestamp = int(first_date.timestamp())
    second_timestamp = int(second_date.timestamp())
    random_timestamp = random.randint(first_timestamp, second_timestamp)
    return datetime.fromtimestamp(random_timestamp).date()

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
    for item in app_tables.group_table.search():
        row = add_row(item)
        data.append(row)
    return data

def get_group_color():
  return random.choice("blue green yellow red".split())

@anvil.server.callable
def add_group(group_name, group_description):
  app_tables.group_table.add_row(group_name=group_name,
                                 group_description=group_description
                                )

@anvil.server.callable
def delete_group(table_entry):
  table_entry.delete()