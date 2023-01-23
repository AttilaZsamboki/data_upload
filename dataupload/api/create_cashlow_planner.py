import psycopg2
from datetime import date, timedelta


def create_cashflow_planner():
    DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
    DB_NAME = "defaultdb"
    DB_USER = "doadmin"
    DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
    DB_PORT = "25060"
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
    current_categories = list(cur.fetchone())
    if current_categories[0] is not None:
        current_categories = current_categories[0].split(
            ", ")
    else:
        current_categories = []
    cur.execute('select distinct name, elem_tipus from elemek;')
    all_data = [list(i) for i in cur.fetchall()]
    all_categories = [i[0] for i in all_data]
    for i in current_categories:
        if i in all_categories:
            continue
        else:
            cur.execute(
                f"delete from cashflow_planner_table where name = '{i}'")
            conn.commit()
    for i in all_data:
        if i[0] in current_categories:
            continue
        for day in days:
            cur.execute(
                f"insert into cashflow_planner_table (name, day, planned_expense, tipus) values ('{i[0]}', '{day}', 0, '{i[1]}')")
            conn.commit()
    cur.close()
    conn.close()


create_cashflow_planner()
