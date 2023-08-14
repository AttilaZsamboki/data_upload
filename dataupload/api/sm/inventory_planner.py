import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from sqlalchemy import create_engine
from datetime import datetime
from datetime import datetime
from .send_vendor_order import send_vendor_order
from .fetch_data import sm_fetch_data
from ..utils.utils import log
import requests
from .download_order import download_order

import django
import os
import sys

sys.path.append(os.path.abspath('/home/atti/googleds/dataupload'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "dataupload.settings")
django.setup()
from api.models import SMVendorOrders, SMVendorsTable, SMOrderQueue  # noqa


DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

channel_layer = get_channel_layer()


async def send_message(status, progress_value=0):
    await channel_layer.group_send(
        'sm_order',
        {
            'type': 'order_status_change',
            'message': status,
            'progress_value': progress_value
        }
    )


def inventory_planner(vendor, status, is_new, id=0):
    # create
    currency = SMVendorsTable.objects.filter(name=vendor)[
        0].budget_currency
    if status == "DRAFT":
        # generate random id
        id = datetime.now().strftime('%Y%m%d%H%M%S')
        # make it more unique
        id = int(id + str(datetime.now().microsecond))

        new_order = SMVendorOrders(id=id,
                                   vendor=vendor, order_status=status, created_date=datetime.now(), currency=currency)
        new_order.save()
        async_to_sync(send_message)("Rendelés letöltése", 10)
        order_dict = SMVendorOrders.objects.filter(id=id)
        download_order(vendor)
        SMOrderQueue.objects.filter(
            vendor=vendor, status="NEW").update(status="ADDED", order_id=id)
        async_to_sync(send_message)("Draft sikeresen összeállítva", 100)
        log(status="SUCCESS", log_value=new_order)
        return {"status": "SUCCESS", "message": new_order, "id": id}
    # create | update
    order_dict = SMVendorOrders.objects.filter(id=id)
    if status == "OPEN":
        async_to_sync(send_message)("Rendelés összerakása megkezdődött", 0)
        # - 0%
        if is_new:
            SMVendorOrders(id=id,
                           vendor=vendor, order_status=status, created_date=datetime.now(), currency=currency).save()
        order_dict.update(order_status=status)
        async_to_sync(send_message)(
            "Inventory Planner adatok lekérdezése", 3)
        # - 30% - 33%
        sm_fetch_data()
        async_to_sync(send_message)("Rendelés letöltése", 34.5)
        # - 2% - 1%
        po = send_vendor_order(
            vendor, status, send_message, currency)
        if po["status"] == "ERROR":
            log(status="FAILED", log_value=po["message"])
            return po
        po_reference = po["reference"]
        new_id = po["id"]
        value = ""
        SMOrderQueue.objects.filter(
            vendor=vendor, status="ADDED" if not is_new else "NEW").update(order_id=None)
        order_dict.update(id=new_id, reference=po_reference, open_date=datetime.now(
        ), total=po["total"], total_ordered=po["total_ordered"])
        order_dict = SMVendorOrders.objects.filter(id=new_id)
        SMOrderQueue.objects.filter(
            vendor=vendor, status="ADDED" if not is_new else "NEW").update(status="SENT", order_id=new_id)
        value = {"id": new_id, "reference": po_reference}
        async_to_sync(send_message)("Termék adatok frissítése", 70.5)
        # - 29% - 30%
        sm_fetch_data()
        async_to_sync(send_message)("Rendelés sikeresen létrehozva", 100)
        log(status="SUCCESS", log_value=value)
        return {"status": "SUCCESS", "message": value}
    if status == "CLOSED" or status == "CANCELLED":
        async_to_sync(send_message)(
            "Inventory Planner Purchase Order státusz frissítése folyamatban", 0)
        payload = {
            "purchase-order": {
                "status": status,
                "skip_background_jobs": False,
            }
        }
        response = requests.put(url=f"https://app.inventory-planner.com/api/v1/purchase-orders/{id}", json=payload, headers={
            "Authorization": "219fd6d79ead844c1ecaf1d86dd8c2bb38862e4cd96f7ae95930d605b544126d", "Account": "a3060"
        })
        if response.status_code == 200:
            value = "Order {} for {} updated".format(
                status, vendor)
            log(status="SUCCESS", log_value=value)
            async_to_sync(send_message)(
                "Inventory Planner Purchase Order státusz sikeresen frissítve", 100)
            return {"status": "SUCCESS", "message": value}
        else:
            value = "Order {} for {} failed to update. Error".format(
                status, vendor, response.text)
            log(status="FAILED", log_value=value)
            return {"status": "ERROR", "message": value}
