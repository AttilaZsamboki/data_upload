import pandas as pd
from psycopg2 import connect
from sqlalchemy import create_engine


file = r"C:\Users\GAMERPCX\Downloads\Untitled 1.xlsx"
data = pd.read_excel(file)

keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 60,
    "keepalives_interval": 10,
    "keepalives_count": 5
}

DB_HOST = "db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com"
DB_NAME = "POOL1"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25061"

engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                       "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

conn = connect(dbname=DB_NAME, user=DB_USER,
               password=DB_PASS, host=DB_HOST, port=DB_PORT, **keepalive_kwargs)
cur = conn.cursor()

sourceColumnNames = ["Name", "Date"]

columnNames = {}



data.to_sql("temporary", engine, index=False)
cur.execute("INSERT INTO test_table ("+", ".join(["\""+i+"\"" for i in columnNames.keys()]) +
            ") SELECT "+", ".join(["\""+i+"\"" for i in columnNames.values()])+" FROM temporary;")
conn.commit()

cur.execute("DROP TABLE temporary;")
conn.commit()

cur.close()
conn.close()
