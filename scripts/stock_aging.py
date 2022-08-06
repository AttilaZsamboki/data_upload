from datetime import datetime
from time import strptime
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://doadmin:AVNS_FovmirLSFDui0KIAOnu@db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require")

stock_report = pd.read_sql_table(
    table_name="fol_stock_transaction_report", con=engine)
stock_report.sort_values(by="Finished", ascending=False, inplace=True)
stock_report.dropna(subset=['Finished'], inplace=True)

skus = {}

for row in stock_report.iloc:
    sku = row["Product"]
    quantity = row["Quantity"]
    finished = row["Finished"]
    shippment_supplier_name = row["Shipment_supplier_name"]

    if sku not in skus:
        skus[sku] = [[quantity, finished, shippment_supplier_name]]
    else:
        skus[sku].append([quantity, finished, shippment_supplier_name])

stock_transaction_report = pd.read_sql_table(
    table_name="fol_stock_report", con=engine)

stock_report_obj = {}

for row in stock_transaction_report.iloc:
    sku = row["sku"]

    if sku in skus and sku not in stock_report_obj:
        stock_report_obj[sku] = {"on_stock": row["on_stock"],
                                 "inventory_value_layer": row["inventory_value_layer"], "on_stock_layer": row["on_stock_layer"]}
    elif sku in skus and sku in stock_report_obj:
        stock_report_obj[sku]["on_stock"] = row["on_stock"]
        stock_report_obj[sku]["inventory_value_layer"] += row["inventory_value_layer"]
        stock_report_obj[sku]["on_stock_layer"] += row["on_stock_layer"]

for sku, stock_report_info in stock_report_obj.items():
    skus[sku].append(stock_report_info)

stock_aging = {"sku": [], "shipment": [], "shipment_now": [], "current_stock": [], "date": [],
               "age": [], "weighted_archimetric_mean": [], "shipment_supplier_name": []}

for sku, infos in skus.items():
    if sku != '-' and sku is not None:
        current_stock = infos[-1]["on_stock"]
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
                    stock_aging["current_stock"].append(infos[-1]["on_stock"])
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
                    stock_aging["current_stock"].append(infos[-1]["on_stock"])
                    stock_aging["age"].append(shipment_date)
                    stock_aging["weighted_archimetric_mean"].append(
                        inventory_value_layer / on_stock_layer if on_stock_layer else 0)
                    stock_aging["date"].append(date)
                    stock_aging["shipment_supplier_name"].append(i[2])
                    stock_aging["shipment"].append(shipment)
                    current_stock = abs(shipment - current_stock)

df = pd.DataFrame(stock_aging)
df.to_sql("fol_stock_aging", engine, if_exists="replace")
