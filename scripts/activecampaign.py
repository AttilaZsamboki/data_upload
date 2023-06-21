import requests
import pandas as pd
from sqlalchemy import create_engine

DB_HOST = 'defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com'
DB_NAME = 'defaultdb'
DB_USER = 'doadmin'
DB_PASS = 'AVNS_FovmirLSFDui0KIAOnu'
DB_PORT = '25060'

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

df = pd.read_sql("""select distinct "Billing_Email", "Customer_Identifier"
from fol_orders
where "Sku" in (select cikkszam from fol_unas_extended where "1_alkategoria" = '3D Csempematrica') and "Billing_Email" = 'agnes.gondor@gmail.com'""", con=engine)

print(df)
url = "https://foliasjucihu.api-us1.com/api/3/ecomCustomers"

for i in df.iloc:
    payload = {"ecomCustomer": {
        "connectionid": "1",
        "externalid": "6666666",
        "email": i.Billing_Email,
        "acceptsMarketing": "1"
    }}
    print(payload)

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Api-Token": "8964abf3f791ed0367e9ef97ef82d36144f810ad1fb957294037dc3fc506abf298593c1e"
    }

    response = requests.post(url, json=payload, headers=headers)
