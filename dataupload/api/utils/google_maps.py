import os
import googlemaps
import dotenv
from .logs import log
dotenv.load_dotenv()


def calculate_distance(start, end, mode="driving"):
    gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))
    try:
        direction_result = gmaps.directions(
            start, end, mode=mode)
    except googlemaps.exceptions.ApiError as e:
        log("Hiba a Google Maps API-al való kommunikáció során",
            status="ERROR", script_name="calculate_distance", details=e)
        return {"distance": 0, "duration": 0}
    distance = direction_result[0]['legs'][0]['distance']['value']
    duration = direction_result[0]['legs'][0]['duration']['value']
    return {"distance": distance, "duration": duration}
