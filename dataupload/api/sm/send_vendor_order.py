from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine
from ..utils.gmail import send_message, service
import pandas as pd
import requests
import os

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)


def send_vendor_order(vendor, status, currency="HUF"):
    directory = '/home/atti/googleds/files/sm_pos/{}'.format(
        vendor)
    if not os.path.exists(directory):
        os.makedirs(directory)
    path = directory + "/{}.xlsx".format(
        datetime.now().strftime('%Y-%m-%d'))
    pd.read_sql(f"""select sku, sum(to_order) as quantity
                    from (select sku, to_order
                        from sm_product_data
                        where vendor like '{vendor}'
                            and to_order > 0
                            and sku not like '%%5M%%'
                        union
                        select sku, quantity
                        from sm_order_queue
                        where vendor like '{vendor}') as combined
                    group by 1""", con=engine).to_excel(
        path, index=False)
    email_address, email_body, email_subject = pd.read_sql(
        f"select email_address, email_body, email_subject from sm_vendors_table where name = '{vendor}';", con=engine).iloc[0]
    if email_address is not None and email_subject is not None and email_body is not None and email_address != "" and email_subject != "" and email_body != "":
        send_message(service=service,
                     destination=email_address, obj=email_subject, body=email_body, attachment=path)
    else:
        return {"status": "ERROR", "message": "Rosszul megadott email adatok '{}' beszállítónál".format(vendor)}
    payload = {
        "purchase-order": {
            "status": status,
            "expected_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            "vendor": vendor,
            "warehouse": "c23867_csv.606f0e8dc97c0",
            "currency": currency.upper(),
            "variants_filter": {
                "vendor": vendor,
                "to_order_gt": 0
            },
            "skip_background_jobs": False,
        }
    }
    response = requests.post(url=f"https://app.inventory-planner.com/api/v1/purchase-orders", json=payload, headers={
        "Authorization": "219fd6d79ead844c1ecaf1d86dd8c2bb38862e4cd96f7ae95930d605b544126d", "Account": "a3060"})
    if response.status_code == 500:
        return {"status": "ERROR", "message": response.json()["result"]["message"]}
    response = response.json()
    return response["purchase-order"]
