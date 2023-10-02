from datetime import datetime
import pandas as pd
from psycopg2 import connect
from sqlalchemy import create_engine
from os import environ
from dotenv import load_dotenv
load_dotenv()

DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_PORT = environ.get("DB_PORT")

engine = create_engine('postgresql://'+DB_USER+':' +
                        DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

conn = connect(dbname=DB_NAME, user=DB_USER,
               password=DB_PASS, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

stock_transaction_report = pd.read_sql(
    "select * from fol_stock_transaction_report_ext;", con=engine)
stock_transaction_report.sort_values(
    by="Finished", ascending=False, inplace=True)
stock_transaction_report = stock_transaction_report[
    stock_transaction_report["Related_identifier"].str[:2] != "RET"]
stock_transaction_report.dropna(subset=['Finished'], inplace=True)

skus = {}

for row in stock_transaction_report.iloc:
    sku = row["Product"]
    quantity = row["Quantity"]
    finished = row["Finished"]
    shippment_supplier_name = row["Shipment_supplier_name"]

    if sku not in skus:
        skus[sku] = [[quantity, finished, shippment_supplier_name]]
    else:
        skus[sku].append([quantity, finished, shippment_supplier_name])

stock_report = pd.read_sql_table(
    table_name="fol_stock_report", con=engine)

stock_report = stock_report.query(
    f"timestamp == '{stock_report['timestamp'].max()}'")
stock_report_obj = {}

for row in stock_report.iloc:
    sku = row["sku"]

    if sku in skus and sku not in stock_report_obj:
        stock_report_obj[sku] = {"on_stock": row["on_stock"],
                                 "inventory_value_layer": row["inventory_value_layer"], "on_stock_layer": row["on_stock_layer"]}
    elif sku in skus and sku in stock_report_obj:
        stock_report_obj[sku]["on_stock"] = row["on_stock"]
        stock_report_obj[sku]["inventory_value_layer"] += row["inventory_value_layer"]
        stock_report_obj[sku]["on_stock_layer"] += row["on_stock_layer"]

for sku in skus.keys():
    if sku in stock_report_obj.keys():
        skus[sku].append(stock_report_obj[sku])
    else:
        skus[sku].append(
            {"on_stock": 0, "inventory_value_layer": 0, "on_stock_layer": 0})

stock_aging = {"sku": [], "shipment": [], "shipment_now": [], "current_stock": [], "date": [],
               "age": [], "weighted_archimetric_mean": [], "shipment_supplier_name": []}

for sku, infos in skus.items():
    if sku != '-' and sku is not None:
        current_stock = infos[-1]["on_stock"]
        if current_stock > 0:
            inventory_value_layer = infos[-1]["inventory_value_layer"]
            on_stock_layer = infos[-1]["on_stock_layer"]
            for i in infos:
                if type(i) is list:
                    shipment = i[0]
                    shipment_date = datetime.now() - \
                        datetime.strptime(
                            str(i[1]), "%Y-%m-%d %H:%M") if str(i[1]) != 'nan' else 'nan'
                    date = datetime.strptime(
                        str(i[1]), "%Y-%m-%d %H:%M") if str(i[1]) != 'nan' else 'nan'
                    shipment_date = shipment_date.days

                    if shipment >= current_stock and current_stock:
                        stock_aging["sku"].append(sku)
                        stock_aging["shipment_now"].append(current_stock)
                        stock_aging["current_stock"].append(
                            infos[-1]["on_stock"])
                        stock_aging["age"].append(shipment_date)
                        stock_aging["weighted_archimetric_mean"].append(
                            inventory_value_layer / on_stock_layer if on_stock_layer else 0)
                        stock_aging["date"].append(date)
                        stock_aging["shipment_supplier_name"].append(i[2])
                        stock_aging["shipment"].append(shipment)
                        break
                    else:
                        stock_aging["sku"].append(sku)
                        stock_aging["shipment_now"].append(shipment)
                        stock_aging["current_stock"].append(
                            infos[-1]["on_stock"])
                        stock_aging["age"].append(shipment_date)
                        stock_aging["weighted_archimetric_mean"].append(
                            inventory_value_layer / on_stock_layer if on_stock_layer else 0)
                        stock_aging["date"].append(date)
                        stock_aging["shipment_supplier_name"].append(i[2])
                        stock_aging["shipment"].append(shipment)
                        current_stock = abs(shipment - current_stock)

df = pd.DataFrame(stock_aging)
cur.execute("truncate fol_stock_aging")
conn.commit()
cur.close()
conn.close()
df.to_sql("fol_stock_aging", engine, if_exists="append")
