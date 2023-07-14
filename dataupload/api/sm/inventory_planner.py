import os
from sqlalchemy import create_engine
from datetime import datetime
from datetime import datetime
from .send_vendor_order import send_vendor_order
from .fetch_data import sm_fetch_data
from ..utils.logs import log
import requests

import django
import os
import sys

sys.path.append(os.path.abspath('/home/atti/googleds/dataupload'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "dataupload.settings")
django.setup()
from api.models import SMVendorOrders, SMVendorsTable  # noqa


DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)


def inventory_planner(vendor, status, is_new, id=0):
    # create
    if status == "DRAFT":
        # generate random id
        id = datetime.now().strftime('%Y%m%d%H%M%S')
        # make it more unique
        id = int(id + str(datetime.now().microsecond))
        value = new_order = SMVendorOrders(id=id,
                                           vendor=vendor, order_status=status, created_date=datetime.now())
        new_order.save()
        log(status="SUCCESS", log_value=value)
        return {"status": "SUCCESS", "message": value}
    # create | update
    if status == "OPEN":
        sm_fetch_data()
        currency = SMVendorsTable.objects.filter(name=vendor)[
            0].budget_currency
        po = send_vendor_order(vendor, status, currency)
        if po["status"] == "ERROR":
            log(status="FAILED", log_value=po["message"])
            return po
        po_reference = po["reference"]
        new_id = po["id"]
        value = ""
        if not is_new:
            value = {"id": new_id, "reference": po_reference}
            # update
            SMVendorOrders.objects.filter(
                id=id).update(id=new_id, order_status=status, reference=po_reference, total=po["total"], total_ordered=po["total_ordered"], currency=currency)
        else:
            value = "{} order created for {}, reference number {}".format(
                status, vendor, po_reference)
            SMVendorOrders(vendor=vendor, order_status=status,
                           reference=po_reference, created_date=datetime.now(), id=new_id, total=po["total"], total_ordered=po["total_ordered"], currency=currency).save()
        sm_fetch_data()
        log(status="SUCCESS", log_value=value)
        return {"status": "SUCCESS", "message": value}
    if status == "CLOSED" or status == "CANCELLED":
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
            if status == "CLOSED":
                SMVendorOrders.objects.filter(
                    id=id).update(order_status=status, completed_date=datetime.now().strftime('%Y-%m-%d'))
            elif status == "CANCELLED":
                SMVendorOrders.objects.filter(
                    id=id).update(order_status=status, cancelled_date=datetime.now().strftime('%Y-%m-%d'))
            log(status="SUCCESS", log_value=value)
            return {"status": "SUCCESS", "message": value}
        else:
            value = "Order {} for {} failed to update".format(
                status, vendor)
            log(status="FAILED", log_value=value)
            return {"status": "ERROR", "message": value}
