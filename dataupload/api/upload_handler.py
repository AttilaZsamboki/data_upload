import pandas as pd
import unidecode
import psycopg2
from sqlalchemy import create_engine

# database connection


def handle_uploaded_file(file, table, special_queries, table_template, extension_format):

    keepalive_kwargs = {
        "keepalives": 1,
        "keepalives_idle": 60,
        "keepalives_interval": 10,
        "keepalives_count": 5
    }

    DB_HOST = "db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com"
    DB_NAME = "defaultdb"
    DB_USER = "doadmin"
    DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
    DB_PORT = "25060"

    engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                           "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"?sslmode=require")

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT, **keepalive_kwargs)
    cur = conn.cursor()

    p_key_column = table_template.pkey_col
    table = table_template.table

    # data -->> pandas dataframe
    # skipping rows
    if extension_format == 'csv':
        data = pd.read_csv(file, skiprows=int(table_template.skiprows))
    elif extension_format == 'tsv':
        data = pd.read_csv(file, skiprows=int(
            table_template.skiprows), delimiter='\t')
    else:
        data = pd.read_excel(file, skiprows=int(table_template.skiprows))

    df = pd.DataFrame(data)

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

    df.to_sql("temporary", engine, index=False)

    for query in special_queries:
        cur.execute(query.special_query)
        conn.commit()

    if not table_template.append:
        cur.execute("TRUNCATE "+table+";")
        cur.execute("INSERT INTO "+table+" SELECT * FROM temporary;")
        conn.commit()
    else:
        # selecting rows that are in both the temporary and permanent table
        cur.execute("INSERT INTO "+table+" SELECT * FROM temporary WHERE \"" +
                    p_key_column+"\" NOT IN (SELECT \""+p_key_column+"\" FROM "+table+");")
        conn.commit()

    # dropping temporary table
    cur.execute("DROP TABLE temporary;")
    conn.commit()

    # closing connection
    cur.close()
    conn.close()