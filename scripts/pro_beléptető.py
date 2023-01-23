import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    'mysql://profibarkacs_belepteto:aEe8cMiPkiJjjQcK@s07.devent.hu/profibarkacs_belepteto')

engine2 = create_engine(
    'postgresql://doadmin:AVNS_FovmirLSFDui0KIAOnu@defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com:25060/defaultdb?sslmode=require')

df = pd.read_sql("select * from events", engine)
con = engine2.connect()
con.execute("truncate pro_belepteto")
df.to_sql(name="pro_belepteto", con=engine2, if_exists="append")
