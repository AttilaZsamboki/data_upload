import requests
import math
import dotenv
import os
from ..utils.google_maps import calculate_distance
dotenv.load_dotenv()

API_KEY = os.environ.get("PEN_MINICRM_API_KEY")
SYSTEM_ID = os.environ.get("PEN_MINICRM_SYSTEM_ID")
telephely = "Budapest, Nagytétényi út 218, 1225"

data = requests.get(
    'https://r3.minicrm.hu/Api/R3/Project/41444', auth=(SYSTEM_ID, API_KEY)
).json()

address = data['Cim2']
gmaps_result = calculate_distance(start=telephely, end=address)
duration = gmaps_result["duration"] / 60
distance = gmaps_result["distance"] // 1000
print(f"Distance: {distance} km")
formatted_duration = f"{math.floor(duration//60)} óra {math.floor(duration%60)} perc"

update = requests.put(
    'https://r3.minicrm.hu/Api/R3/Project/41444', auth=(SYSTEM_ID, API_KEY), json={"UtazasiIdoKozponttol": formatted_duration, "Tavolsag": distance})
