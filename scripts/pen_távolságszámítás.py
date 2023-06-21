import googlemaps
import pandas as pd
from sqlalchemy import create_engine
import googlemaps
from datetime import datetime
import re

with open("/home/atti/googleds/logs/pen/útszámítás.log", "w") as log:
    log.write(str(datetime.now()))

DB_HOST = 'defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com'
DB_NAME = 'defaultdb'
DB_USER = 'doadmin'
DB_PASS = 'AVNS_FovmirLSFDui0KIAOnu'
DB_PORT = '25060'

engine = create_engine('postgresql://'+DB_USER+':' +
                       DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

# set up a client object with your API key
gmaps = googlemaps.Client(key='AIzaSyDfR747PvOqM5a5YlWW7uEdEJFi6mVPvz0')

df = pd.read_sql(
    """
    select *
        from pen_adatlapok_rendezett
        where "Adatlap_Azonosito" not in (select id from pen_kiszállások)
            and "Adatlap_Azonosito" not in (select id from pen_útszámítás_errors)
            and "Adatlap_Cim:" is not null
  """, con=engine)

telephely = "Budapest, Nagytétényi út 218, 1225"
current_day = {}
last_at = {}
obj = []


def log_error():
    pd.DataFrame([{"id": i["Adatlap_Azonosito"], "date": datetime.now(), "error": "Hibásan megadott cím"}]).to_sql("pen_útszámítás_errors",
                                                                                                                   con=engine, index=False, if_exists="append")


for i in df.iloc:
    address = re.sub(r"\b[Ff][Ss][Zz]\b\.?\s*\d*\.?",
                     "", i["Adatlap_Cim:"])
    if not current_day or i["Adatlap_Ki_epitette_be?"] not in current_day.keys():
        try:
            direction_result = gmaps.directions(
                telephely, address, mode="driving")
        except (googlemaps.exceptions.ApiError):
            log_error()
            continue
        distance = direction_result[0]['legs'][0]['distance']['value']
        duration = direction_result[0]['legs'][0]['duration']['value']
        obj.append({"nap": i["Adatlap_Beepites_Idopontja"], "honnan": telephely, "hova": address, "kihez": i["Adatlap_Nev"],
                    "kik": i["Adatlap_Ki_epitette_be?"], "ut_hossz_m": distance, "ut_hossz_s": duration, "id": i["Adatlap_Azonosito"], "adatlap_url": i["Adatlap_URL"]})
    elif current_day[i["Adatlap_Ki_epitette_be?"]] == i["Adatlap_Beepites_Idopontja"].strftime("%Y-%m-%d"):
        try:
            direction_result = gmaps.directions(last_at[i["Adatlap_Ki_epitette_be?"]], address,
                                                mode="driving")
        except (googlemaps.exceptions.ApiError):
            log_error()
            continue
        distance = direction_result[0]['legs'][0]['distance']['value']
        duration = direction_result[0]['legs'][0]['duration']['value']
        obj.append({"nap": i["Adatlap_Beepites_Idopontja"], "honnan": last_at[i["Adatlap_Ki_epitette_be?"]], "hova": address, "kihez": i["Adatlap_Nev"],
                    "kik": i["Adatlap_Ki_epitette_be?"], "ut_hossz_m": distance, "ut_hossz_s": duration, "id": i["Adatlap_Azonosito"], "adatlap_url": i["Adatlap_URL"]})
    else:
        try:
            direction_result = gmaps.directions(last_at[i["Adatlap_Ki_epitette_be?"]], telephely,
                                                mode="driving")
        except (googlemaps.exceptions.ApiError):
            log_error()
            continue
        distance = direction_result[0]['legs'][0]['distance']['value']
        duration = direction_result[0]['legs'][0]['duration']['value']
        obj.append({"nap": current_day[i["Adatlap_Ki_epitette_be?"]] + " 17:00:00.000000", "honnan": last_at[i["Adatlap_Ki_epitette_be?"]], "hova": telephely, "kihez": "",
                    "kik": i["Adatlap_Ki_epitette_be?"], "ut_hossz_m": distance, "ut_hossz_s": duration, "id": ""})
        direction_result = gmaps.directions(
            telephely, address, mode="driving")
        distance = direction_result[0]['legs'][0]['distance']['value']
        duration = direction_result[0]['legs'][0]['duration']['value']
        obj.append({"nap": i["Adatlap_Beepites_Idopontja"], "honnan": telephely, "hova": address, "kihez": i["Adatlap_Nev"],
                    "kik": i["Adatlap_Ki_epitette_be?"], "ut_hossz_m": distance, "ut_hossz_s": duration, "id": i["Adatlap_Azonosito"], "adatlap_url": i["Adatlap_URL"]})
    current_day[i["Adatlap_Ki_epitette_be?"]
                ] = i["Adatlap_Beepites_Idopontja"].strftime("%Y-%m-%d")
    last_at[i["Adatlap_Ki_epitette_be?"]] = address

df2 = pd.DataFrame(obj)
df2.to_sql("pen_kiszállások", con=engine, index=False, if_exists="append")
