import pandas as pd
from sqlalchemy import create_engine
import requests
import json
from datetime import timedelta, datetime
import os

with open("/home/atti/googleds/logs/tmd_output.log", "w") as log:
    log.write(str(datetime.now() + timedelta(hours=1)))
package_types = {"F": "Fólia", "CS": "Csempematrica",
                 "FP": "Falpadló", "P": "Padló"}
DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"
API_KEY = "Uw8lch7DxJAueRPVfvBmNYM92pab1odE"
SYSTEM_ID = "47845"
USER_ID = 75012
CATEGORY_ID = 49
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                       "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

df = pd.read_sql(
    """select * from fol_orders where "Order_Id" like 'ORD-%%' and "Sku" like '%%TMD%%' and "Order_Id" not in (select order_id from tmd_processed_orders) and "Order_Status" = 'Completed'""", con=engine)

for row in df.iloc():
    contact_id = 0
    type_of_package = "".join(
        [j for i, j in package_types.items() if i == row.Sku[-1]])
    response = requests.get(
        f'https://r3.minicrm.hu/Api/R3/Contact?Email={row.Billing_Email}', auth=(SYSTEM_ID, API_KEY))
    if response.status_code == 200:
        response = json.loads(response.content)
        if len(response["Results"]):
            contact_id = next(iter(response["Results"]))
        else:
            response = os.popen(
                f'curl -s --user "{SYSTEM_ID}":"{API_KEY}" -XPUT "https://r3.minicrm.hu/Api/R3/Contact/" -d \'{{"Type": "Person", "FirstName": "{row.Shipping_First_Name}", "LastName": "{row.Shipping_Last_Name}", "Email": "{row.Billing_Email}"}}\'').read()
            try:
                contact_id = response["Id"]
            except:
                print("ERROR! LINE 45", contact_id)
    response = os.popen(
        f'curl -s --user "{SYSTEM_ID}":"{API_KEY}" -XPUT "https://r3.minicrm.hu/Api/R3/Project/" -d \'{{"Name":"{row.Shipping_Last_Name} {row.Shipping_First_Name} ({type_of_package})","UserId":75012,"CategoryId":49,"ContactId":{contact_id},"StatusId":3210}}\'').read()
    adatlap_id = json.loads(response)["Id"]
    os.system(f'curl -s --user "{SYSTEM_ID}":"{API_KEY}" -XPUT "https://r3.minicrm.hu/Api/R3/Project/{adatlap_id}" -d \'{{"RendelesAzonosito2":"{row.Order_Id}","RendeltDoboz":"{type_of_package}","Kezbesitve":"{row.Completed_Date}","VisszakuldesIdopontja":"{row.Completed_Date+timedelta(days=5)}","Zip":"{row.Shipping_Zip_Code}","City":"{row.Shipping_City}","Address":"{row.Shipping_Address_1}"}}\'')

    pd.DataFrame(data={"order_id": [row.Order_Id], "status": ["completed"]}).to_sql(
        "tmd_processed_orders", if_exists="append", index=False, con=engine)
else:
    pass
