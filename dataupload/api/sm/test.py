import requests

response = requests.get(url=f"https://app.inventory-planner.com/api/v1/purchase-orders/64abf3bda3bdb39b1c0b2f75", headers={
    "Authorization": "219fd6d79ead844c1ecaf1d86dd8c2bb38862e4cd96f7ae95930d605b544126d", "Account": "a3060"
})

print(response.json()["purchase-order"]["status"])
