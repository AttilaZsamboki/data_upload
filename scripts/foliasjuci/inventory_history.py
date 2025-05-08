import pandas as pd
from sqlalchemy import create_engine
from os import environ
from dotenv import load_dotenv

load_dotenv()

DB_HOST = environ.get("DB_HOST")
DB_NAME = environ.get("DB_NAME")
DB_USER = environ.get("DB_USER")
DB_PASS = environ.get("DB_PASS")
DB_PORT = environ.get("DB_PORT")

engine = create_engine(
    "postgresql://"
    + DB_USER
    + ":"
    + DB_PASS
    + "@"
    + DB_HOST
    + ":"
    + DB_PORT
    + "/"
    + DB_NAME
    + "?sslmode=require"
)

data = pd.read_sql(
    sql="""
        select CURRENT_TIMESTAMP as time, 
                "1_alkategoria", 
                sum(stock.inventory_value_layer) as inventory_value,
                count(distinct stock.sku) as sku,
                sum(aging.age * current_stock) / sum(current_stock) as age,
                avg(fsn_nap) as fsn,
                sum("Quantity") as sales
        from fol_unas_extended unas
        left join fol_stock_report_last stock on stock.sku = unas.cikkszam
        left join (select sku, current_stock, avg(age) age from fol_stock_aging_ext group by 1, 2) aging on unas.cikkszam = aging.sku
        left join (select * from "forgásisebesség_összesítés" where stat_end = (select max(stat_end) from "forgásisebesség_összesítés")) "forgásisebesség_összesítés" on "forgásisebesség_összesítés".sku = unas.cikkszam
        left join (select * from fol_order_item where "Order_Date" >= (select max(time::date) from fol_inventory_history)) as orders on orders."Sku" = unas.cikkszam
        where "1_alkategoria" in ('Öntapadós fólia',
                'Ablakfólia',
                '3D Csempematrica',
                'Falpanel',
                'Padló',
                'Eszközök')
        group by 2
    """,
    con=engine,
)

data.to_sql("fol_inventory_history", con=engine, if_exists="append", index=False)
