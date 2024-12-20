from psycopg2 import connect

DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"


def col_by_dtype(data_type, curr_table):
    conn = connect(dbname=DB_NAME, user=DB_USER,
                   password=DB_PASS, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()
    data_type_str = ""
    for i in range(len(data_type)):
        if i != len(data_type)-1:
            data_type_str += "'" + data_type[i] + "',"
        else:
            data_type_str += "'" + data_type[i] + "'"
    cur.execute("""select string_agg(col.column_name, ', ')
    from information_schema.columns col
            join information_schema.tables tab on tab.table_schema = col.table_schema
        and tab.table_name = col.table_name
        and tab.table_type = 'BASE TABLE'
    where col.data_type in ("""+data_type_str+""")
    and col.table_name = '"""+curr_table+"""'
    group by col.table_schema;""")
    try:
        return list(cur.fetchone())[0].split(", ")
    except:
        return None
