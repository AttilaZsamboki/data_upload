import pandas as pd
import unidecode
import psycopg2
from sqlalchemy import create_engine
import os
from .models import DatauploadUploadmodel, DatauploadTabletemplates, DatauploadTableOverview
from .utils.upload import col_by_dtype
from json import dumps
from datetime import date, datetime
from .utils.gmail import send_message, gmail_authenticate

service = gmail_authenticate()


def handle_uploaded_file(file, table, table_template, user_id, is_new_table, column_bindings, is_feed, is_email=None, sender_email=None):
    errors = []
    if not is_new_table:
        skiprows = table_template.skiprows
    else:
        skiprows = 0
    upload_model = DatauploadUploadmodel.objects.get(
        file=file, table=table, user_id=user_id, status="ready")
    upload_model.status_description = "Feldolgozás alatt"
    upload_model.status = "under upload"
    upload_model.save()
    null_cols = [i for i, j in column_bindings.items() if j == '']
    for i in null_cols:
        del column_bindings[i]

    filename, extension_format = os.path.splitext(str(file))

    keepalive_kwargs = {
        "keepalives": 1,
        "keepalives_idle": 60,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }

    DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
    DB_NAME = "defaultdb"
    DB_USER = "doadmin"
    DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
    DB_PORT = "25060"

    engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                           "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT, **keepalive_kwargs)
    cur = conn.cursor()
    column_binding_values_str = "".join(column_bindings.values())

    #\\\\\\\\\\\\\\\\\\\\\\\\\ data -->> pandas dataframe ///////////////////////////////////////////#
    if extension_format == '.csv':
        data = pd.read_csv(file, skiprows=int(skiprows))
    elif extension_format == '.tsv':
        data = pd.read_csv(file, skiprows=int(
            table_template.skiprows), delimiter='\t')
    else:
        data = pd.read_excel(file, skiprows=int(skiprows))

    df = pd.DataFrame(data)

    source_column_names = df.columns
    # \\\\\\\\\\\\\\\\\\\\\\\\\ table specifics ///////////////////////////////////////////////
    if table in ["fol_stock_report", "pro_stock_report"]:
        if is_feed:
            df["timestamp"] = date.today()
        else:
            df["timestamp"] = filename[-10:]
        column_bindings["timestamp"] = "timestamp"

    if table == 'fol_gls_elszámolás':
        df = df[df['Súly'].notna()]
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
            template = DatauploadTabletemplates(table=table, pkey_col="", skiprows=skiprows,
                                                append="Felülírás", source_column_names=dumps(column_bindings))
            template.save()
            df.to_sql(table, engine, index=False)
            cur.execute(f"TRUNCATE {table}")
            conn.commit()
            os.remove('/home/atti/googleds/dataupload/media/' + str(file))
            upload_log = DatauploadUploadmodel.objects.get(
                table=table, file=file, user_id=user_id)
            upload_log.status = "success"
            upload_log.status_description = "Sikeres létrehozott tábla!"
            upload_log.save()
            table_overview = DatauploadTableOverview(
                db_table=table, verbose_name=table.title().replace("_", " "), available_at="upload")
            table_overview.save()
            return
        else:
            upload_model = DatauploadUploadmodel.objects.get(
                file=file, table=table, user_id=user_id)
            upload_model.status_description = f"Tábla már létezik{table}"
            upload_model.status = "error"
            upload_model.save()
            return print(f"Tábla már létezik '{table}'")

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
        date_cols = col_by_dtype(
            ['date', 'timestamp', 'timestamp without time zone'], table)
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
            except (ValueError, psycopg2.errors.DatatypeMismatch) as e:
                upload_model = DatauploadUploadmodel.objects.get(
                    file=file, table=table, user_id=user_id)
                upload_model.status_description = f"Egy hiba lépett fel a(z) '{i}' oszlop tartalmát illetően: {e}"
                upload_model.status = "error"
                upload_model.save()
                if is_email:
                    send_message(service, sender_email, "Rossz tábla tartalom",
                                 f"Egy hiba lépett fel a(z) '{i}' oszlop tartalmát illetően: {e}")
                    os.remove(str(file))
                return

    if "temporary" in tables_in_sql:
        cur.execute("DROP TABLE temporary;")
        conn.commit()

    df.to_sql("temporary", engine, index=False)

    for i in column_bindings.values():
        if i not in df.columns:
            print(i + " not in source file, check your template")
            errors.append(
                f"{i} oszlop nincs benne a fájlban, biztosítsd azt, hogy benne van és próbáld újra")
        if errors:
            if is_email:
                send_message(service, sender_email, "Feltöltésben akadt hibák", f"""Az alábbi hibák akadtak a feltöltésben: {", ".join(errors)}.

                                A fenti okok miatt a feltöltés törlésre került.
                                """)

    base_query = "INSERT INTO \""+table+"\" ("+", ".join(["\""+i+"\"" for i in column_bindings.keys(
    )]) + ") SELECT "+", ".join(["\""+i+"\"" for i in column_bindings.values()])+" FROM temporary" if column_binding_values_str else "INSERT INTO "+table+" SELECT * FROM temporary"

    if table_template.append == "Felülírás":
        cur.execute("TRUNCATE \""+table+"\";")
        conn.commit()
    elif table_template.append == "Hozzáfűzés duplikációk szűrésével":
        primary_key_source = table_template.pkey_col
        primary_key_db = "".join(
            [i for i, j in column_bindings.items() if j == primary_key_source])
        cur.execute(
            f"DELETE FROM {table} WHERE \"{primary_key_db}\" IN (SELECT \"{primary_key_source}\" FROM temporary);")
        conn.commit()
    try:
        cur.execute(base_query)
    except psycopg2.errors.UndefinedColumn as e:
        upload_model.status = "error"
        upload_model.status_description = f"Hibás oszlop nevek ({e})"
        upload_model.save()
        return
    conn.commit()

    # dropping temporary table
    cur.execute("DROP TABLE temporary;")
    conn.commit()

    # closing connection
    cur.close()
    conn.close()

    upload_model = DatauploadUploadmodel.objects.get(
        file=file, table=table, user_id=user_id, status="under upload")
    upload_model.status_description = "Sikeres feltöltés!"
    upload_model.status = "success"
    file_dir = f"/home/atti/googleds/files/{table}/"
    if not os.path.isdir(file_dir):
        os.mkdir(file_dir)
    if not is_email and not is_feed:
        files_already_existing = [f for f in os.listdir(
            file_dir) if f"{date.today()}" in f]
        upload_model.file = f"{file_dir}{str(filename).split('/')[-1]}{f' ({len(files_already_existing)-1})' if files_already_existing else ''}{extension_format}"
        os.rename("/home/atti/googleds/dataupload/media/" + str(file),
                  str(upload_model.file))
    elif is_email:
        send_message(service, sender_email, "Sikeres feltöltés",
                     f"Feltöltésed ({filename.split('/')[-1]}) sikeresen felkerült az adatbázisba")
    upload_model.save()