import pandas as pd
import unidecode
import psycopg2
import datetime as dt
from sqlalchemy import create_engine
import os
from .models import DatauploadUploadmodel
# database connection


def handle_uploaded_file(file, table, special_queries, table_template, extension_format, user_id, is_new_table, skiprows):

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

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT, **keepalive_kwargs)
    cur = conn.cursor()

    # data -->> pandas dataframe
    # skipping rows
    if extension_format == 'csv':
        data = pd.read_csv(file, skiprows=int(skiprows))
    elif extension_format == 'tsv':
        data = pd.read_csv(file, skiprows=int(
            table_template.skiprows), delimiter='\t')
    else:
        data = pd.read_excel(file, skiprows=int(skiprows))

    df = pd.DataFrame(data)

    if table in ["fol_stock_report", "pro_stock_report"]:
        df["timestamp"] = dt.datetime.now()

    # # renaming unicode columns to ascii
    column_names = {}
    # this is not the best choice, maybe there are better modules
    chars_to_replace = {": ": "_", " ": "_",
                        "(": "", ")": "", "%": "", ".": "", "\'": "", "-": "_"}
    for i in df.columns:
        # ascii
        column_names[i] = unidecode.unidecode(i)
        for l, j in chars_to_replace.items():
            # removing additional character
            column_names[i] = column_names[i].replace(l, j)
    for i, l in column_names.items():
        df.rename(columns={i: l}, inplace=True)

    cur.execute("SELECT string_agg(tablename, ', ') FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    tables_in_sql = list(cur.fetchone())[0].split(", ")

    if is_new_table:
        if table not in tables_in_sql:
            df.to_sql(table, engine, index=False)
            cur.execute("TRUNCATE "+table)
            conn.commit()
            os.remove('/home/atti/googleds/dataupload/media/' + str(file))
            DatauploadUploadmodel.objects.get(
                table=table, file=file, user_id=user_id).delete()
            return
        else:
            return print("Table already exists")

    if table not in tables_in_sql:
        if table.capitalize() in tables_in_sql:
            table = table.capitalize()
        elif table.lower() in tables_in_sql:
            table = table.lower()
        else:
            return print("Hibásan megadott táblanév, nincs ilyen tábla az adatbázisban!")

    def col_by_dtype(data_type, curr_table):
        data_type_str = ""
        for i in range(len(data_type)):
            if i != len(data_type)-1:
                data_type_str += "'" + data_type[i] + "',"
            else:
                data_type_str += "'" + data_type[i] + "'"
        cur.execute("""select lower(string_agg(col.column_name, ', '))
        from information_schema.columns col
                join information_schema.tables tab on tab.table_schema = col.table_schema
            and tab.table_name = col.table_name
            and tab.table_type = 'BASE TABLE'
        where col.data_type in ("""+data_type_str+""")
        and col.table_name = '"""+curr_table+"""'
        group by col.table_schema;""")
        try:
            cols = list(cur.fetchone())[0].split(", ")
            cols = [i.lower() for i in cols]
            return cols
        except:
            return None

    for i in df.columns:
        if table in tables_in_sql:

            numeric_cols = col_by_dtype(['decimal', 'numeric', 'real', 'double precision',
                                        'smallserial', 'serial', 'bigserial', 'money', 'bigint'], table)
            date_cols = col_by_dtype(['date', 'timestamp'], table)
            try:
                if (numeric_cols is not None) and i.lower() in numeric_cols:
                    lst = []
                    for x in df[i]:
                        if type(x) == str and ',' in x:
                            lst.append(x.replace(',', '.'))
                        else:
                            lst.append(x)
                    df[i] = lst
                    df[i] = df[i].astype(float)
                if (date_cols is not None) and i.lower() in date_cols:
                    df[i] = df[i].astype(dtype='datetime64[ns]')
            except ValueError as e:
                return print(
                    "Egy hiba lépett fel az egyik sor tartalmát illetően:\n", e)

    if "temporary" in tables_in_sql:
        cur.execute("DROP TABLE temporary;")
        conn.commit()

    df.to_sql("temporary", engine, index=False)

    for query in special_queries:
        cur.execute(query.special_query)
        conn.commit()

    cur.execute("""SELECT
                    string_agg(column_name, ', ')
                FROM
                    information_schema.columns
                WHERE
                    table_schema = 'public'
                    AND table_name = '"""+table+"""';""")
    sql_columns = list(cur.fetchone())[0].split(", ")

    if table_template.append == "Felülírás":
        cur.execute("TRUNCATE "+table+";")
        cur.execute("INSERT INTO "+table+" SELECT * FROM temporary;")
        conn.commit()
    elif table_template.append == "Hozzáfűzés duplikációk szűrésével":
        p_key_column = table_template.pkey_col
        if p_key_column in sql_columns:
            p_key_column_sql = p_key_column
        else:
            if p_key_column.lower() in sql_columns:
                p_key_column_sql = p_key_column.lower()
            elif p_key_column.capitalize() in sql_columns:
                p_key_column_sql = p_key_column.capitalize()
            else:
                cur.execute("DROP TABLE temporary;")
                conn.commit()
                cur.close()
                conn.close()
                return print("Hibásan megadott elsődleges kulcs!")

        if p_key_column in df.columns:
            p_key_column_df = p_key_column
        else:
            if p_key_column.lower() in df.columns:
                p_key_column_df = p_key_column.lower()
            elif p_key_column.capitalize() in df.columns:
                p_key_column_df = p_key_column.capitalize()
            else:
                cur.execute("DROP TABLE temporary;")
                conn.commit()
                cur.close()
                conn.close()
                return print("Hibásan megadott elsődleges kulcs!")

        cur.execute("INSERT INTO "+table+" SELECT * FROM temporary WHERE \"" +
                    p_key_column_df+"\" NOT IN (SELECT \""+p_key_column_sql+"\" FROM "+table+");")
    elif table_template.append == "Hozzáfűzés":
        cur.execute("INSERT INTO "+table+" SELECT * FROM temporary;")
        conn.commit()

    # dropping temporary table
    cur.execute("DROP TABLE temporary;")
    conn.commit()

    # closing connection
    cur.close()
    conn.close()

    os.remove('/home/atti/googleds/dataupload/media/' + str(file))
    DatauploadUploadmodel.objects.get(
        table=table, file=file, user_id=user_id).delete()
