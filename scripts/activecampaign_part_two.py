import urllib.parse
from sqlalchemy import create_engine
import pandas as pd
import requests
import json

DB_HOST = 'defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com'
DB_NAME = 'defaultdb'
DB_USER = 'doadmin'
DB_PASS = 'AVNS_FovmirLSFDui0KIAOnu'
DB_PORT = '25060'

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

df = pd.read_sql("""select "Billing_Email" as email,
       "Webshop_Id"    as externalid,
       "Currency"      as currency,
       "Order_Date"    as date,
       "Order_Total"   as total_price,
       "Order_Id"
from fol_order_base
where "Billing_Email" = 'agnes.gondor@gmail.com'
    """, con=engine)

print(df)
url = "https://foliasjucihu.api-us1.com/api/3/ecomOrders"


for i in df.iloc:

    df2 = pd.read_sql(f"""
                select "Product_Name"                   as fuck_name,
       round("Unit_Price" / "Quantity") as price,
       "Quantity"                       as quantity,
       "Sku"                            as externalid,
       "1_alkategoria"                  as category,
       "Kep_link"                       as image
from fol_order_item
         left join fol_unas_extended on "Sku" = cikkszam
where "Order_Id" = '{i.Order_Id}'
    """, con=engine)
    order_products = []
    for j in df2.iloc:
        order_products.append({"name": j.fuck_name, "price": j.price *
                              100, "quantity": j.quantity, "externalid": j.externalid, "category": j.category, "imageUrl": j.image})

    exturl = f"https://foliasjucihu.api-us1.com/api/3/ecomCustomers?filters[email]={urllib.parse.quote(i.email)}"

    extheaders = {
        "accept": "application/json",
        "Api-Token": "8964abf3f791ed0367e9ef97ef82d36144f810ad1fb957294037dc3fc506abf298593c1e"
    }

    extres = requests.get(exturl, headers=extheaders)

    externalid = json.loads(extres.text)["ecomCustomers"][1]["id"]
    payload = {"ecomOrder": {
        "orderProducts": order_products,  # CORRECT
        "externalid": i["externalid"],  # CORRECT
        "source": 1,  # CORRECT
        "email": i.email,  # CORRECT
        "connectionid": 1,  # CORRECT
        "customerid": externalid,
        "totalPrice": i.total_price * 100,  # CORRECT
        "currency": i.currency,  # CORRECT
        "externalCreatedDate": str(i.date)  # CORRECT
    }}

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Api-Token": "8964abf3f791ed0367e9ef97ef82d36144f810ad1fb957294037dc3fc506abf298593c1e"
    }

    print(payload)
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
