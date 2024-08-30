import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import connect

DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"

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

keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 60,
    "keepalives_interval": 10,
    "keepalives_count": 5,
}

conn = connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    **keepalive_kwargs
)
cur = conn.cursor()

data = pd.read_sql(
    sql="""
with in_stock_days as (select sku,
                              current_date as start,
                              min(date)    as end,
                              count(*)     as in_stock_days
                       from forgásisebesség_részletező
                       where on_stock > 0
                       group by 1, 2),
     on_stock as (select sku, sum(on_stock_layer) as on_stock
                  from fol_stock_report
                  where timestamp = (select max(timestamp) from fol_stock_report)
                  group by 1),
     agg_funnel as (select forgásisebesség_részletező.sku,
                           min(date)                                              as stat_start,
                           current_date                                           as stat_end,
                           sum(forgásisebesség_részletező.cogs)                   as cogs,
                           sum(forgásisebesség_részletező.sales)                  as sales,
                           avg(forgásisebesség_részletező.average_inventory_cost) as avg_inv_cost,
                           avg(forgásisebesség_részletező.average_inventory)      as avg_inv
                    from forgásisebesség_részletező
                    group by 1, 3)
select stat_start,
       current_date as stat_end,
       agg_funnel.sku,
       agg_funnel.cogs,
       agg_funnel.sales,
       avg_inv_cost,
       in_stock_days,
       agg_funnel.sales / nullif(avg_inv, 0)                     as stockturn_ip,
       avg_inv_cost * in_stock_days / nullif(agg_funnel.cogs, 0) as fsn_nap,
       agg_funnel.cogs / nullif(avg_inv_cost, 0)                 as fsf_fordulat,
       agg_funnel.sales / in_stock_days                          as sales_velocity,
       case
           when fol_product_suppliers."Supplier___1___Default" = 1
               then "Supplier___1___Lead_Time"
           else "Supplier___2___Lead_Time"
           end                                                   as lead_time,
       case
           when fol_product_suppliers."Supplier___1___Default" = 1
               then "Supplier___1___Days_of_Stock"
           else "Supplier___2___Days_of_Stock"
           end                                                   as days_of_stock,
       on_stock.on_stock
from agg_funnel
         left join on_stock on on_stock.sku = agg_funnel.sku
         left join fol_product_suppliers on fol_product_suppliers."SKU" = agg_funnel.sku
         left join in_stock_days on in_stock_days.sku = agg_funnel.sku
""",
    con=engine,
)

data.to_sql("forgásisebesség_összesítés", con=engine, if_exists="append")
