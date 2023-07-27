import requests
import json
import os
import dotenv
dotenv.load_dotenv()

API_KEY = os.environ.get("PEN_MINICRM_API_KEY")
SYSTEM_ID = os.environ.get("PEN_MINICRM_SYSTEM_ID")

costumers = [
    # {"contact_name": "Tesztelő János", "name": "ML2023-E/00010 (E-munkalap)"},
    {"contact_name": "Teszt Mackó", "name": "ML2023-E/00011 (E-munkalap)"},
]

# for i in costumers:
#     contact = requests.get(
#         'https://r3.minicrm.hu/Api/R3/Contact', params={"Name": i["contact_name"]}, auth=(SYSTEM_ID, API_KEY)).json()
#     print(json.dumps(contact, indent=4))
#     contact_id = list(contact["Results"].keys())[0]
#     data = requests.get(
#         'https://r3.minicrm.hu/Api/R3/Project', params={"MainContactId": contact_id, "CategoryId": 28, "Name": i["name"]}, auth=(SYSTEM_ID, API_KEY)
#     )
#     print(data.json())
#     user_id = list(data.json()["Results"].keys())[0]
#     print(user_id)

xml = """
<?xml version="1.0" encoding="UTF-8" ?>
<Projects>
    <Project Id="1234567890">
        <Name>Példa adatlap neve</Name>
        <StatusId>3018</StatusId>
        <ContactId>49670</ContactId>
        <UserId>39636</UserId>
        <CategoryId>28</CategoryId>
        <Contacts>
            <Contact Id="49670">
                <Name>Test Mackó</Name>
                <Type>Person</Type>
                <Email>zsamboki+tesztmacko@gmail.com</Email>
                <Phone>+36201234567</Phone>
            </Contact>
        </Contacts>
    </Project>
</Projects>
"""

update = requests.post(
    f'https://{SYSTEM_ID}:{API_KEY}@r3.minicrm.hu/Api/SyncFeed/119/Upload', auth=(SYSTEM_ID, API_KEY), data=xml)

print(update.headers)
