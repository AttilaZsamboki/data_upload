import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import connect
from datetime import date

DB_HOST = "db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"

engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                       "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

conn = connect(dbname=DB_NAME, user=DB_USER,
               password=DB_PASS, host=DB_HOST, port=DB_PORT)

cur = conn.cursor()

költségek = pd.read_sql_table("fol_költségek", engine)
bevételek = pd.read_sql_table("fol_bevételek", engine)

cf_starting_closing = {"honap": [], "nyito": [], "zaro": []}

nyito = 0

months = pd.date_range('2022-01-01', date.today(),
                       freq='MS').strftime("%Y-%m").tolist()

for month in months:
    költség_per_month = 0
    bevételek_per_month = 0
    for row in költségek.iloc:
        if row.honap == month:
            költség_per_month += row.osszesen_huf
    for row in bevételek.iloc:
        if row.Date.strftime("%Y-%m") == month:
            bevételek_per_month += row.Osszesen_HUF
    zaro = nyito + (bevételek_per_month - költség_per_month)
    cf_starting_closing["honap"].append(month)
    cf_starting_closing["nyito"].append(nyito)
    cf_starting_closing["zaro"].append(zaro)
    nyito = zaro


df = pd.DataFrame(cf_starting_closing)
cur.execute("TRUNCATE starting_colsing_cf;")
conn.commit()
df.to_sql("starting_colsing_cf", if_exists='append', index=False)
