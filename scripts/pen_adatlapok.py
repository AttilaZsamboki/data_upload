import os
import requests

API_KEY = "9FrxqTQvICJH3NdZSgRejYf0Kc8kVnaA"
SYSTEM_ID = 119

params = {
    'MainContactId': '34032',
}

response = requests.get(
    'https://r3.minicrm.hu/Api/R3/Project',
    # params=params,
    auth=(SYSTEM_ID, API_KEY),
)

print(response.text)
