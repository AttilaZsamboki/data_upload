import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import connect
from datetime import date

DB_HOST = "195.201.130.156"
DB_NAME = "posgres"
DB_USER = "postgres"
DB_PASS = "9Hq4orC8ehuznXvryOz3HxvVYzzAo96OzSTEx1IPwH5vIlVqbEXgw1XmHf26JXfx"
DB_PORT = "25060"

engine = create_engine(
'postgres://postgres:9Hq4orC8ehuznXvryOz3HxvVYzzAo96OzSTEx1IPwH5vIlVqbEXgw1XmHf26JXfx@195.201.130.156:25060/postgres'
)

conn = connect(dbname=DB_NAME, user=DB_USER,
               password=DB_PASS, host=DB_HOST, port=DB_PORT)

cur = conn.cursor()

költségek = pd.read_sql("select * from fol_költségek_extended", engine)
bevételek = pd.read_sql("select * from fol_bevételek_extended", engine)

cf_starting_closing = {"months": [],
                       "starting_values": [], "closing_values": []}

nyito = 0

months = pd.date_range('2022-01-01', date.today(),
                       freq='MS').strftime("%Y-%m").tolist()

for month in months:
    költség_per_month = 0
    bevételek_per_month = 0
    for row in költségek.iloc:
        if row.date.strftime("%Y-%m") == month:
            költség_per_month += row.osszesen_huf
    for row in bevételek.iloc:
        if row.Date.strftime("%Y-%m") == month:
            bevételek_per_month += row.Osszesen_HUF
    zaro = nyito + (bevételek_per_month - költség_per_month)
    cf_starting_closing["months"].append(month)
    cf_starting_closing["starting_values"].append(nyito)
    cf_starting_closing["closing_values"].append(zaro)
    nyito = zaro
df = pd.DataFrame(cf_starting_closing)

cur.execute("TRUNCATE starting_closing_cf;")
conn.commit()
df.to_sql("starting_closing_cf", engine, if_exists='append', index=False)
