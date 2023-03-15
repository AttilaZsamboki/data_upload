import json
import requests

url = "https://foliasjucihu.api-us1.com/api/3/ecomOrders?filters[externalid]=494726"

headers = {
    "accept": "application/json",
    "Api-Token": "8964abf3f791ed0367e9ef97ef82d36144f810ad1fb957294037dc3fc506abf298593c1e"
}

num_iterations = 10
for i in range(0, num_iterations):
    response = requests.get(url, headers=headers)
    id_ = [i["id"] for i in json.loads(response.text)["ecomOrders"]]

    print(json.loads(response.text)["meta"]["total"])
    for i in id_:
        del_url = f"https://foliasjucihu.api-us1.com/api/3/ecomOrders/{i}"

        del_headers = {
            "accept": "application/json",
            "Api-Token": "8964abf3f791ed0367e9ef97ef82d36144f810ad1fb957294037dc3fc506abf298593c1e"
        }

        del_response = requests.delete(del_url, headers=del_headers)
