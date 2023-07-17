import requests
import json


def get_item():
    response = requests.get(url=f"https://app.inventory-planner.com/api/v1/purchase-orders/64b231e24df57b027e0ef1cb/items/c1097_6060", headers={
        "Authorization": "219fd6d79ead844c1ecaf1d86dd8c2bb38862e4cd96f7ae95930d605b544126d", "Account": "a3060"
    })

    print(json.dumps(response.json()["item"], indent=4, sort_keys=True))


def make_po():
    payload = {
        "purchase-order": {
            "status": "OPEN",
            "expected_date": "2023-07-19",
            "vendor": "konrad hornschuch ag",
            "warehouse": "c23867_csv.606f0e8dc97c0",
            "currency": "EUR",
            "items": [
                {
                    "id": "c1097_6060",
                    "replenishment": 16,
                    "vendor": "konrad hornschuch ag",
                },
            ],
            "skip_background_jobs": False,
        }
    }
    response = requests.post(url=f"https://app.inventory-planner.com/api/v1/purchase-orders", json=payload, headers={
        "Authorization": "219fd6d79ead844c1ecaf1d86dd8c2bb38862e4cd96f7ae95930d605b544126d", "Account": "a3060"
    })
    print(response.json())


get_item()
