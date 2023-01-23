import requests

headers = {
    'accept': 'application/json',
    'apikey': 'i5zl7bkushb2ar7ovkkpmumpi2y5abpr',
}

params = {
    '_perPage': '10',
    '_sortField': 'dateFinished',
    '_sortDir': 'ASC',
}

response = requests.get(
    'http://vincentkompanycompany.com/api/reports/calls/agentsavailability', params=params, headers=headers)
print(response.content)
