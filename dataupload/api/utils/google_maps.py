import os
import googlemaps
import dotenv
dotenv.load_dotenv()

def calculate_distance(start, end, mode="driving"):
    gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))
    direction_result = gmaps.directions(
        start, end, mode=mode)
    distance = direction_result[0]['legs'][0]['distance']['value']
    duration = direction_result[0]['legs'][0]['duration']['value']
    return {"distance": distance, "duration": duration}
