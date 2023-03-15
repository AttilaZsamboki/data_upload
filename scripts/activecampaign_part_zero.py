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

df = pd.read_sql("""select distinct "Billing_Email", "Billing_First_Name", "Billing_Last_Name"
from fol_orders
where "Sku" in (select cikkszam from fol_unas_extended where "1_alkategoria" = '3D Csempematrica') and "Billing_Email" = 'timea.csirmaz@tpaqi.com'
""", con=engine)

contacts = []
for i in df.iloc:
    contacts.append({"email": i.Billing_Email,
                    "first_name": i.Billing_First_Name, "last_name": i.Billing_Last_Name, "subscribe": [{"listid": "4"}]})

url = "https://foliasjucihu.api-us1.com/api/3/import/bulk_import"

payload = {
    "contacts": contacts,
}
headers = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "Api-Token": "8964abf3f791ed0367e9ef97ef82d36144f810ad1fb957294037dc3fc506abf298593c1e"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
