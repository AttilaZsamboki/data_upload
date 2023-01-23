import pandas as pd
import requests
import json
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from psycopg2 import connect


def start_status(single):
    if single:
        cur.execute(
            f"insert into pro_activison_per_agent(agent_id, start_date, status) values ('{i['id']}', '{datetime.now() + timedelta(hours=1)}', '{status}')")
        return conn.commit()
    return pd.DataFrame(data={"start_date": [datetime.now() + timedelta(hours=1)], "end_date": [None]}).to_sql(
        "pro_activison", index=False, if_exists="append", con=engine)


DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"

engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                       "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

conn = connect(dbname=DB_NAME, user=DB_USER,
               password=DB_PASS, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()

# Getting the data
headers = {
    'accept': 'application/json',
    'apikey': '2z0o15ovm3wwd013ugwapx5qm8j62dif',
}
params = {
    '_page': '1',
    '_perPage': '10',
    '_sortDir': 'ASC',
    '_from': '0',
    '_to': '0',
}

urletf = 'http://profibarkacs.ladesk.com/api/onlinestatus/agents'
resp_mf = requests.get(
    urletf, params={"apikey": "MadMdxTGhxWnpjkWOOBwwnLl3alWC8wP"})
content = json.loads(resp_mf.content.decode(
    "utf-8"))["response"]["agentsOnlineStates"]

is_online = False
for i in content:
    if "P" in i["onlineStatus"]:
        is_online = True

# Updating database
df = pd.read_sql_table("pro_activison", con=engine)
df.sort_values(
    by="end_date", ascending=False, inplace=True)
if len(df.index) > 0:
    if is_online:
        if not (df["end_date"].isna()).any():
            start_status(single=False)
    else:
        if (df["end_date"].isna()).any():
            if not (pd.to_datetime(df.sort_values(by="start_date", ascending=False).head(1).start_date, infer_datetime_format=True) < datetime.strptime(f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} 00:00:01", "%Y-%m-%d %H:%M:%S")).bool():
                cur.execute(
                    "update pro_activison set end_date = now() + interval '1 hour' where end_date is null;")
                conn.commit()
else:
    if is_online:
        start_status(single=False)

df3 = pd.read_sql_table("pro_activison_per_agent", con=engine)
for i in content:
    status = i["onlineStatus"]
    if i["id"] in df3["agent_id"].tolist():
        if (pd.to_datetime(df3.loc[df3["agent_id"] == i["id"]].sort_values(by="start_date", ascending=False).head(1).start_date, infer_datetime_format=True) < datetime.strptime(f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} 00:00:01", "%Y-%m-%d %H:%M:%S")).bool():
            cur.execute(
                f"update pro_activison_per_agent set end_date = now() + interval '1 hour' where end_date is null and agent_id = '{i['id']}'")
            conn.commit()
            start_status(single=True)
        elif not (df3.loc[df3["agent_id"] == i["id"]].sort_values(
                by="start_date", ascending=False).head(1).status == status).bool():
            cur.execute(
                f"update pro_activison_per_agent set end_date = now() + interval '1 hour' where end_date is null and agent_id = '{i['id']}'")
            conn.commit()
            cur.execute(
                f"insert into pro_activison_per_agent(agent_id, start_date, status) values ('{i['id']}', '{datetime.now() + timedelta(hours=1)}', '{status}')")
            conn.commit()
    else:
        start_status(single=True)

cur.close()
conn.close()
