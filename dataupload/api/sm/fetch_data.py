import sys
from sqlalchemy import create_engine
import json
import requests
import pandas as pd
import os
import django
from datetime import datetime

sys.path.append(os.path.abspath('/home/atti/googleds/dataupload'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "dataupload.settings")
django.setup()
from api.models import Logs  # noqa
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)


def log(log_value, status="SUCCESS", script_name="sm_vendor_orders"):
    log = Logs(script_name=script_name,
               time=datetime.now(), status=status, value=log_value)
    log.save()


def sm_fetch_data():

    def getVendor(connections):
        if len(connections) == 0 or isinstance(connections, dict):
            if connections["removed"] == False:
                vendors = connections["vendors"][0]["vendor"]
                return vendors
            else:
                return None
        else:
            for i in connections:
                if i["removed"] == False:
                    vendors = i["vendors"][0]["vendor"]
                    return vendors

    page = 0
    engine.execute("delete from sm_product_data")
    while True:
        params = {'page': page, 'limit': '100',
                  "fields": "sku,replenish_date,to_order,forecasted_lost_revenue_lead_time,connections,to_order_cost,id",
                  }
        response = json.loads(requests.get(url=f"https://app.inventory-planner.com/api/v1/variants", params=params, headers={
            "Authorization": os.environ.get("INVENTORY_PLANNER_API"), "Account": "a3060"}).text)
        print(
            f"{round(response['meta']['start'] / response['meta']['total'] * 100, ndigits=0)}%")

        if len(response["variants"]) == 0:
            break
        data = response["variants"]
        newData = []
        for i in range(len(data)):
            newNewData = {}
            newNewData = data[i]["warehouse"][0]
            newNewData["sku"] = data[i]["sku"]
            newNewData["vendor"] = data[i]["connections"]
            newNewData["id"] = data[i]["id"]
            newData.append(newNewData)

        df = pd.DataFrame(newData)
        df["vendor"] = df["vendor"].apply(
            lambda x: getVendor(x))
        df.drop(["warehouse"], axis=1, inplace=True)
        df = df[df["vendor"].notna()]
        df.to_sql("sm_product_data", engine, if_exists='append', index=False)
        page += 1
    log(status="SUCCESS", log_value="Inventoy Planner Data Fetched",
        script_name="sm_fetch_data")
