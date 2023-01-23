from sqlalchemy import create_engine

DB_HOST = 'defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com'
DB_NAME = 'defaultdb'
DB_USER = 'doadmin'
DB_PASS = 'AVNS_FovmirLSFDui0KIAOnu'
DB_PORT = '25060'

engine = create_engine('postgresql://'+DB_USER+':'+DB_PASS +
                       '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME+'?sslmode=require')

con = engine.connect()
con.execute("""update pro_activison_per_agent
                set end_date = (current_date || ' 16:00:00')::timestamp
                where end_date is null""")
con.execute("""update pro_activision
                set end_date = (current_date || ' 16:00:00')::timestamp
                where end_date is null""")
