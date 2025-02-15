from asgiref.sync import async_to_sync
import sys
import django
from datetime import datetime, timedelta
import requests
import os
from sqlalchemy import create_engine
from ..utils.gmail import send_email, gmail_authenticate
import pandas as pd
import numpy as np
import dotenv
from .download_order import download_order

dotenv.load_dotenv()

sys.path.append(os.path.abspath("/home/atti/googleds/dataupload"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataupload.dataupload.settings")
django.setup()

from api.models import SMProductData, FolProductSuppliers  # noqa

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

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


def send_vendor_order(vendor, status, send_message, currency="HUF"):
    data, path = download_order(vendor).values()
    async_to_sync(send_message)("Inventory Planner Purchase Order létrehozása", 36)
    # - 31% - 26%
    items = []
    for i in data.iterrows():
        id = SMProductData.objects.filter(sku=i[1]["sku"]).values()[0]["id"]
        item_details = FolProductSuppliers.objects.filter(sku=i[1]["sku"]).values()[0]
        unit_price = 0
        if item_details["supplier_1_default"] == 1:
            unit_price = item_details["supplier_1_net_price"]
        elif item_details["supplier_2_default"] == 1:
            unit_price = item_details["supplier_2_net_price"]
        items.append(
            {
                "id": id,
                "replenishment": int(i[1]["quantity"]),
                "vendor": vendor,
                "cost_price": unit_price,
                "title": item_details["product_name"],
                "sku": i[1]["sku"],
            }
        )
    payload = {
        "purchase-order": {
            "status": status,
            "expected_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "vendor": vendor,
            "warehouse": "c23867_csv.606f0e8dc97c0",
            "currency": currency.upper(),
            "items": items,
            "skip_background_jobs": False,
        }
    }
    try:
        response = requests.post(
            url=f"https://app.inventory-planner.com/api/v1/purchase-orders",
            json=payload,
            headers={
                "Authorization": "219fd6d79ead844c1ecaf1d86dd8c2bb38862e4cd96f7ae95930d605b544126d",
                "Account": "a3060",
            },
        )
    except:
        return {"status": "ERROR", "message": "Hiba akadt a rendelés elküldése közben"}
    if response.status_code == 500:
        return {"status": "ERROR", "message": response.json()["result"]["message"]}
    response = response.json()["purchase-order"]
    async_to_sync(send_message)("Email küldése", 64.5)
    # - 5% - 7%
    email_address, email_body, email_subject = pd.read_sql(
        f"select email_address, email_body, email_subject from sm_vendors_table where name = '{vendor}';",
        con=engine,
    ).iloc[0]
    if (
        email_address is not None
        and email_subject is not None
        and email_body is not None
        and email_address != ""
        and email_subject != ""
        and email_body != ""
    ):
        service = gmail_authenticate("foliasjuci")
        send_email(
            service=service,
            destination=email_address,
            obj=email_subject
            + f" 'PO #{response['reference']}' {datetime.now().strftime('%Y-%m-%d')}",
            body=email_body,
            attachment=path,
        )
    else:
        return {
            "status": "ERROR",
            "message": "Rosszul megadott email adatok '{}' beszállítónál".format(
                vendor
            ),
        }
    return {
        "id": response["id"],
        "reference": response["reference"],
        "total": np.sum([i["cost_price"] * i["replenishment"] for i in items]),
        "status": "SUCCESS",
        "total_ordered": np.sum([i["replenishment"] for i in items]),
    }
