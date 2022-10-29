import psycopg2
from datetime import date, timedelta

DB_HOST = "db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com"
DB_NAME = "POOL1"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25061"
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST, port=DB_PORT)
cur = conn.cursor()
start_date = date(2022, 10, 29)
end_date = date(2024, 10, 29)

delta = end_date - start_date

days = []
for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    days.append(day)

cur.execute(
    "select string_agg(distinct name, ', ') from cashflow_planner_table;")
current_categories = list(cur.fetchone())[0].split(", ")
cur.execute('select string_agg(distinct name, \', \') from "Koltsegelemek";')
all_categories = list(cur.fetchone())[0].split(", ")
if current_categories != all_categories:
    for i in current_categories:
        if i in all_categories:
            continue
        else:
            cur.execute(
                f"delete from cashflow_planner_table where name = '{i}'")
            conn.commit()
    for i in all_categories:
        if i in current_categories:
            continue
        else:
            for day in days:
                cur.execute(
                    f"insert into cashflow_planner_table (name, day, planned_expense) values ('{i}', '{day}', 0)")
                conn.commit()
cur.close()
conn.close()
