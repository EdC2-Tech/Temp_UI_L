import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import random
from datetime import datetime, timedelta

from functools import wraps
from time import time

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

def add_row():
    gender = random.choice(["male", "female"])

    row = {
        "gender": gender,
        "name": get_full_name(gender),
        "progress": random.randint(0, 100),
        "rating": random.randint(0, 5),
        "col": random.choice("blue green yellow red".split()),
        "car": random.choice([True, False]),
        "dob": random_date(datetime(1950, 1, 1), datetime.now() - timedelta(days=17 * 365)),
    }
    return row


@anvil.server.callable
@timeit
def get_list_data(n=100):
    data = []
    for i in range(n):
        row = add_row()
        row["id"] = i
        #     row['dob'] = row['dob'].strftime('%d/%m/%Y')
        row["dob"] = row["dob"]
        #     row['datetime_obj'] = datetime.now()
        row["media"] = anvil.BlobMedia("text/plain", b"hey")
        data.append(row)
    return data


@anvil.server.callable
def slow_call():
    from time import sleep

    sleep(2)
