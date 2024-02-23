import os
import sys
from datetime import datetime, timedelta
from os import environ

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from .base_path import base_path
import django

load_dotenv()

sys.path.append(os.path.abspath(f"{base_path}/dataupload"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataupload.dataupload.settings")
django.setup()


def log(
    log_value, status="SUCCESS", script_name="sm_vendor_orders", details="", data=None
):
    from api.models import Logs  # noqa

    log = Logs(
        script_name=script_name,
        time=datetime.now() + timedelta(hours=2),
        status=status,
        value=log_value,
        details=details,
        data=data,
    )
    log.save()


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def connect_to_db():
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_PORT = environ.get("DB_PORT")

    engine = create_engine(
        "postgresql://"
        + DB_USER
        + ":"
        + DB_PASS
        + "@"
        + DB_HOST
        + ":"
        + DB_PORT
        + "/"
        + DB_NAME
    )
    return engine


def schedule_feed_retries(table, retry_number, frequency, file=None):
    from api.models import DatauploadRetries  # noqa

    if retry_number is None or frequency == "1 óra":
        return
    engine = connect_to_db()
    try:
        was_upload = list(
            engine.execute(
                f"SELECT COUNT(*) FROM {table} WHERE timestamp = current_date"
            ).fetchall()[0]
        )[0]
        try:
            num_rows_in_file = len(pd.read_excel(file))
        except:
            num_rows_in_file = 0
        if was_upload and num_rows_in_file == was_upload:
            return
    except:
        pass
    for i in range(1, retry_number + 1):
        log(
            "Újrapróbálkozás beütemezve",
            "INFO",
            "dataupload_schedule_feed_retries",
            f"{table}, {i*2} óra múlva, {i}. alkalommal",
        )
        DatauploadRetries(
            table=table, when=datetime.now() + timedelta(hours=i * 2 + 2)
        ).save(),


def check_feed():
    log("Feed check elkezdődött", "INFO", "dataupload_feed_check")
    from api.models import DatauploadUploadmodel, Feed  # noqa

    period_start = datetime.now() + timedelta(hours=1)
    error = False
    for feed in Feed.objects.filter(frequency="1 nap", runs_at=period_start.hour):
        uploads = DatauploadUploadmodel.objects.filter(
            table=feed.table, upload_timestamp__gte=period_start - timedelta(hours=2)
        )
        if not uploads.exists or uploads.count() == 0:
            error = True
            schedule_feed_retries(
                table=feed.table,
                retry_number=feed.retry_number,
                frequency=feed.frequency,
            )
            log(
                f"A '{feed.table}' feed ismeretlen okokból nem került feltöltésre az utolsó 1 órában. {feed.retry_number}, óránkénti újrapróbálkozás lett beütemezve",
                "ERROR",
                "dataupload_feed_check",
            )
    if not error:
        log(
            "Feed check sikeres, nem volt elmaradt feed az utolsó egy órában",
            "INFO",
            "dataupload_feed_check",
        )
