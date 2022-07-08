from pickle import NONE
from typing import Type
import pandas as pd
import unidecode
import psycopg2
from sqlalchemy import create_engine
from numpy import datetime64

# database connection



def handle_uploaded_file(file, table, connection_details):
    
    keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 60,
    "keepalives_interval": 10,
    "keepalives_count": 5
    }

    DB_HOST = connection_details.host
    DB_NAME = connection_details.database
    DB_USER = connection_details.username
    DB_PASS = connection_details.password
    DB_PORT = connection_details.port

    engine = create_engine(
        "postgresql://"+DB_USER+":"+DB_PASS+"@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT, **keepalive_kwargs)
    cur = conn.cursor()
    
    # getting the primary key
    p_keys = {"Azonosito": ["bevételek"], "azonosito": ["költségek"], "Order_Id": ["orders"], "Szamla_belso_azonosito": [
        "számlák"], "Cikkszam": ["unas"], "Csomagszam": ["gls_elszámolás"], "SKU": ["product_suppliers"], "ID": ["stock_report"]}
    

    p_key_column = ""
    for i, l in p_keys.items():
        for j in l:
            if j == table:
                p_key_column = i
                break

    # data -->> pandas dataframe
    if table != "gls_elszámolás":
        data = pd.read_excel(file)
    # some tables don't start at the first row
    else:
        data = pd.read_excel(file, skiprows=4)
    df = pd.DataFrame(data)

    # duplicate row_name renaming -- poor solution
    if table == "költségek":
        df.rename(columns={"Megjegyzések.1": "Megjegyzések2", "Azonosító": "azonosito"}, inplace=True)

    # renaming unicode columns to ascii
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
    df.rename(columns=column_names, inplace=True)

    # deleting columns from gls report
    if table == "gls_elszámolás":
        cur.execute("""SELECT lower(column_name)
        FROM
            information_schema.columns
        WHERE
            table_schema = 'public'
            AND table_name = 'gls_elszámolás';
        """)
        gls_cols = [", ".join(i) for i in cur.fetchall()]
        for column in data.columns:
            if column.lower() not in gls_cols:
                df.drop(column, inplace=True, axis=1)

    # there are rows that don't identify as int
    # maybe there are better solutions but this is as good as it gets

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
        cur.execute("SELECT string_agg(tablename, ', ') FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
        if table in list(cur.fetchone())[0].split(", "):

            numeric_cols = col_by_dtype(['decimal', 'numeric', 'real', 'double precision',
                                        'smallserial', 'serial', 'bigserial', 'money', 'bigint'], table)
            date_cols = col_by_dtype(['date', 'timestamp'], table)
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

    # unas sub-categories
        # adding the new cols to the end of the dataframe
    if table == "unas":
        df[[str(i)+"_alkategoria" for i in range(1, 6)]
           ] = df["Kategoria"].str.split("|", expand=True)

        # deleting the main categories column
        df.drop("Kategoria", inplace=True, axis=1)

    # adding df to database
    cur.execute("SELECT string_agg(tablename, ', ') FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    df.to_sql("temporary", engine, index=False)

    # selecting rows that are in both the temporary and permanent table
    cur.execute("INSERT INTO "+table+" SELECT * FROM temporary WHERE \"" +
                p_key_column+"\" NOT IN (SELECT \""+p_key_column+"\" FROM "+table+");")
    conn.commit()

    # dropping temporary table
    cur.execute("DROP TABLE temporary;")
    conn.commit()

    #deleting false rows from gls
    if table == "gls_elszámolás":
        cur.execute("DELETE FROM gls_elszámolás WHERE \"Felvetel_datuma_\" IS NULL OR logisztika = 0;")
        conn.commit()

    # closing connection
    cur.close()
    conn.close()