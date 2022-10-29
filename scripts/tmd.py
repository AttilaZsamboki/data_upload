import pandas as pd
from sqlalchemy import create_engine
import requests
import json
from datetime import timedelta

package_types = {"F": "Folia", "CS": "Csempematrica",
                 "FP": "Falpadlo", "P": "Padlo"}
DB_HOST = "db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com"
DB_NAME = "POOL1"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25061"
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
    """select * from fol_orders where "Sku" like '%%TMD%%' and "Order_Id" not in (select order_id from tmd_processed_orders)""", con=engine)

for row in df.iloc():
    contact_id = 0
    type_of_package = "".join(
        [j for i, j in package_types.items() if i == row.Sku[-1]])
    response = requests.get(
        f'https://r3.minicrm.hu/Api/R3/Contact?Email={row.Shipping_Email}', auth=(SYSTEM_ID, API_KEY))
    if response.status_code == 200:
        response = json.loads(response.content)
        if len(response["Results"]):
            contact_id = next(iter(response["Results"]))
        else:
            data = f'{{"Type": "Person", "FirstName": "{row.Shipping_First_Name}", "LastName": "{row.Shipping_Last_Name}", "Email": "{row.Shipping_Email}"}}'
            response = requests.put('https://r3.minicrm.hu/Api/R3/Contact/',
                                    headers=headers, data=data, auth=(SYSTEM_ID, API_KEY))
            if response.status_code == 200:
                contact_id = response.content
            else:
                pass
    data = f'{{"Name":"{row.Order_Id}","UserId":75012,"CategoryId":49,"ContactId":21995,"StatusId":3210}}'
    response = requests.put('https://r3.minicrm.hu/Api/R3/Project/',
                            headers=headers, data=data, auth=(SYSTEM_ID, API_KEY))
    adatlap_id = json.loads(response.content.decode("utf-8"))["Id"]


    data = f'{{"RendelesAzonosito2":"{row.Order_Id}","RendeltDoboz":"{type_of_package}","Kezbesitve":"{row.Completed_Date}","VisszakuldesIdopontja":"{row.Completed_Date+timedelta(days=5)}","Zip":"{row.Shipping_Zip_Code}","City":"{row.Shipping_City}","Address":"{row.Shipping_Address_1}}}'
    response = requests.put(f'https://r3.minicrm.hu/Api/R3/Project/{adatlap_id}',
                            headers=headers, data=data, auth=(SYSTEM_ID, API_KEY))


    print(response.content.decode("utf-8"))
else:
    pass
