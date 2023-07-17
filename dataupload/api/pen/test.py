import json
import requests
import os
import dotenv
dotenv.load_dotenv()

API_KEY = os.environ.get("PEN_MINICRM_API_KEY")
SYSTEM_ID = os.environ.get("PEN_MINICRM_SYSTEM_ID")

data = requests.get(
    'https://r3.minicrm.hu/Api/R3/Schema/Project/28', auth=(SYSTEM_ID, API_KEY)
)

if data.status_code != 400:
    print(", ".join(data.json().keys()))
else:
    print(data.content)
