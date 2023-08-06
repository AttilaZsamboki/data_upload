import sys
import os
import django
from sqlalchemy import create_engine
from os import environ
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime, timedelta
import platform
load_dotenv()


base_path = (
    os.environ.get("BASE_PATH_LINUX")
    if platform.system() == "Linux"
    else os.environ.get("BASE_PATH_WINDOWS")
)


sys.path.append(os.path.abspath(f"{base_path}/dataupload"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "dataupload.dataupload.settings")
django.setup()
from api.models import DatauploadRetries  # noqa


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def connect_to_db():
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_PORT = environ.get("DB_PORT")

    engine = create_engine('postgresql://'+DB_USER+':' +
                           DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)
    return engine


def schedule_feed_retries(table, retry_number, frequency, file=None):
    if retry_number is None or frequency == "1 óra":
        return
    engine = connect_to_db()
    try:
        was_upload = list(engine.execute(
            f"SELECT COUNT(*) FROM {table} WHERE timestamp = current_date").fetchall()[0])[0]
        try:
            num_rows_in_file = len(pd.read_excel(file))
        except:
            num_rows_in_file = 0
        if was_upload and num_rows_in_file == was_upload:
            return
    except:
        pass
    for i in range(1, retry_number+1):
        DatauploadRetries(table=table, when=datetime.now() +
                          timedelta(hours=i*2+2)).save(),
