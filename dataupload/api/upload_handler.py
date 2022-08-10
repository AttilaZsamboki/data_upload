import pandas as pd
import unidecode
import psycopg2
import datetime as dt
from sqlalchemy import create_engine
import os
from .models import DatauploadUploadmodel, DatauploadTabletemplates
from .utils.upload import col_by_dtype
from json import dumps


def handle_uploaded_file(file, table, special_queries, table_template, extension_format, user_id, is_new_table, skiprows, column_bindings):

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

    #\\\\\\\\\\\\\\\\\\\\\\\\\ data -->> pandas dataframe ///////////////////////////////////////////#
    if extension_format == 'csv':
        data = pd.read_csv(file, skiprows=int(skiprows))
    elif extension_format == 'tsv':
        data = pd.read_csv(file, skiprows=int(
            table_template.skiprows), delimiter='\t')
    else:
        data = pd.read_excel(file, skiprows=int(skiprows))

    df = pd.DataFrame(data)

    source_column_names = df.columns
    # \\\\\\\\\\\\\\\\\\\\\\\\\ table specifics ///////////////////////////////////////////////
    if table in ["fol_stock_report", "pro_stock_report"]:
        df["timestamp"] = dt.datetime.now()

    #\\\\\\\\\\\\\\\\\\\\\\ ADDING NEW TABLES /////////////////////////////////////#

    #\\\\\\\\\\\\\\\\\\\\\\\\ UTF-8 >---> ASCII (HEAD) ///////////////////////////////////////#
    cur.execute("SELECT string_agg(tablename, ', ') FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
    tables_in_sql = list(cur.fetchone())[0].split(", ")
    if is_new_table:
        column_names = {}
        chars_to_replace = {": ": "_", " ": "_",
                            "(": "", ")": "", "%": "", ".": "", "\'": "", "-": "_"}
        for i in df.columns:
            column_names[i] = unidecode.unidecode(i)
            for l, j in chars_to_replace.items():
                column_names[i] = column_names[i].replace(l, j)
        for i, l in column_names.items():
            df.rename(columns={i: l}, inplace=True)

        if table not in tables_in_sql:
            db_column_names = df.columns
            column_bindings = {}
            for i in range(len(db_column_names)):
                column_bindings[db_column_names[i]] = source_column_names[i]
            template = DatauploadTabletemplates(table=table, pkey_col="", skiprows=skiprows, created_by_id=user_id,
                                                append="Hozzáfűzés duplikációk szűrésével", extension_format=extension_format, source_column_names=dumps(column_bindings))
            template.save()
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

    if table in tables_in_sql:
        numeric_cols = col_by_dtype(['decimal', 'numeric', 'real', 'double precision',
                                    'smallserial', 'serial', 'bigserial', 'money', 'bigint'], table)
        date_cols = col_by_dtype(['date', 'timestamp'], table)
        numeric_cols_source = [
            j for i, j in column_bindings.items() if i in numeric_cols] if numeric_cols else []
        date_cols_source = [
            j for i, j in column_bindings.items() if i in date_cols] if date_cols else []
    for i in df.columns:
        try:
            if numeric_cols_source and i in numeric_cols_source:
                lst = []
                for x in df[i]:
                    if type(x) == str and ',' in x:
                        lst.append(x.replace(',', '.'))
                    else:
                        lst.append(x)
                df[i] = lst
                df[i] = df[i].astype(float)
            if date_cols_source and i in date_cols_source:
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

    for i in column_bindings.values():
        if i not in df.columns:
            print(i + " not in source file, check your template")

    base_query = "INSERT INTO "+table+" ("+", ".join(["\""+i+"\"" for i in column_bindings.keys(
    )]) + ") SELECT "+", ".join(["\""+i+"\"" for i in column_bindings.values()])+" FROM temporary"

    if table_template.append == "Felülírás":
        cur.execute("TRUNCATE "+table+";")
        cur.execute(base_query)
        conn.commit()
    elif table_template.append == "Hozzáfűzés duplikációk szűrésével":
        primary_key_source = table_template.pkey_col
        primary_key_db = [
            i for i, j in column_bindings.items() if j == primary_key_source]
        cur.execute(base_query + " WHERE \"" +
                    primary_key_source+"\" NOT IN (SELECT \""+"".join(primary_key_db)+"\" FROM "+table+");")
    elif table_template.append == "Hozzáfűzés":
        cur.execute(base_query)
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
