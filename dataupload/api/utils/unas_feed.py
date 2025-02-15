import requests as rq
from xml.etree import ElementTree


def get_unas_token():
    key = "cfcdf8a7109a30971415ff7f026becdc50dbebbd"
    token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{key}</ApiKey></Params>'
    token_request = rq.get("https://api.unas.eu/shop/login", data=token_payload)
    token_tree = ElementTree.fromstring(token_request.content)
    if token_tree[0].tag == "Token":
        global token
        return token_tree[0].text


def get_unas_feed_url(lang="hu"):
    url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Format>xlsx</Format><Lang>{lang}</Lang></Params>'
    token = get_unas_token()
    url_request = rq.get(
        "https://api.unas.eu/shop/getProductDB",
        headers={"Authorization": f"Bearer {token}"},
        data=url_payload,
    )
    url_tree = ElementTree.fromstring(url_request.content)
    url = url_tree[0].text
    return url
