# import os
# import pandas as pd
# from sqlalchemy import create_engine
# from datetime import datetime, timedelta

# DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
# DB_NAME = "defaultdb"
# DB_USER = "doadmin"
# DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
# DB_PORT = "25060"

# engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
#                        "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

# templates = pd.read_sql_table(
#     con=engine, table_name="dataupload_tabletemplates")
# tables = templates[templates["append"] != "Hozzáfűzés"]
# tables = templates[templates["table"].isin(
#     os.listdir("/home/atti/googleds/files"))]
# for table in tables:
#     df = pd.read_sql_table(con=engine, table_name='dataupload_uploadmodel')
#     df = df[df["table"] == table]
#     df = df[df["upload_timestamp"] < datetime.today() - timedelta(days=30)]
#     print(df)
#     # if os.path.exists(str(df.file)):
#     #     os.remove(str(df.file))
