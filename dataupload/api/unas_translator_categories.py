import requests as rq
from xml.etree import ElementTree
import pandas as pd
from sqlalchemy import create_engine


def translate_categories():
    DB_HOST = 'defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com'
    DB_NAME = 'defaultdb'
    DB_USER = 'doadmin'
    DB_PASS = 'AVNS_FovmirLSFDui0KIAOnu'
    DB_PORT = '25060'

    engine = create_engine('postgresql://'+DB_USER+':' +
                           DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

    # --- get token
    key = "cfcdf8a7109a30971415ff7f026becdc50dbebbd"
    token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{key}</ApiKey></Params>'
    token_request = rq.get(
        "https://api.unas.eu/shop/login", data=token_payload)
    token_tree = ElementTree.fromstring(token_request.content)
    if token_tree[0].tag == "Token":
        global token
        token = token_tree[0].text

    # --- get url

    url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Lang>sk</Lang></Params>'
    url_request = rq.get("https://api.unas.eu/shop/getCategory",
                         headers={"Authorization": f"Bearer {token}"}, data=url_payload)

    def etree_to_dict(t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = {}
            for dc in map(etree_to_dict, children):
                for k, v in dc.items():
                    if k in dd:
                        if isinstance(dd[k], list):
                            dd[k].append(v)
                        else:
                            dd[k] = [dd[k], v]
                    else:
                        dd[k] = v
            d = {t.tag: dd}
        if t.attrib:
            d[t.tag].update(('@' + k, v)
                            for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                    d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    xml_string = url_request.content.decode("utf-8")
    root = ElementTree.fromstring(xml_string)
    python_dict = etree_to_dict(root)
    df = pd.DataFrame(python_dict["Categories"]["Category"])
    df = df.drop(columns=list(set(df.columns) - set(["Id", "Name"])))
    engine.execute("truncate fol_unas_categories")
    df.to_sql("fol_unas_categories", con=engine,
              if_exists="append", index=False)


translate_categories()
