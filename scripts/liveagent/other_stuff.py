import json
import requests
from sqlalchemy import create_engine
from datetime import date, datetime, timedelta
import pandas as pd

DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"

engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                       "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

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

start = date.today()
df = pd.DataFrame({}, columns={"id": "agent_id", "answers": "number_of_cases",
                  "newAnswerAvgTime": "response_time", "missed_calls": "missed_calls"})
for i in range(30):
    start_date = (start - timedelta(days=i)
                  ).strftime("%Y-%m-%d") + " 00:00:00"
    end_date = (start - timedelta(days=i-1)).strftime("%Y-%m-%d") + " 00:00:00"
    urletf = f'http://profibarkacs.ladesk.com/api/reports/agents?date_from={start_date}&date_to={end_date}'
    resp_mf = requests.get(
        urletf, params={"apikey": "MadMdxTGhxWnpjkWOOBwwnLl3alWC8wP", "columns": "missed_calls, newAnswerAvgTime, answers"})
    data = json.loads(resp_mf.content.decode("utf-8"))["response"]["agents"]
    for i in data:
        i["start_date"] = start_date
        i["end_date"] = end_date
    df = df.append(data, ignore_index=True)
for index, row in df.iterrows():
    engine.execute(
        f"DELETE FROM pro_liveagent WHERE (id, start_date) = ('{row['id']}', '{row['start_date']}');")
df.to_sql("pro_liveagent", con=engine, if_exists="append")