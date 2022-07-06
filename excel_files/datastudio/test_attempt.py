import psycopg2

DB_HOST = "db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com"
DB_NAME = "defaultdb"
DB_USER = "doadmin"
DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
DB_PORT = "25060"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST, port=DB_PORT)

cur = conn.cursor()

cur.execute("""SELECT lower(string_agg(column_name, ', '))
        FROM
            information_schema.columns
        WHERE
            table_schema = 'public'
            AND table_name = 'gls_elszámolás';
        """)

print(list(cur.fetchone()[0].split(',')))