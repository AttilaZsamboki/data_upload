import pandas as pd
import unicodedata
from xml.etree import ElementTree
from sqlalchemy import create_engine
from .utils.unas_feed import get_unas_feed_url
import requests
import json
import os
import dotenv
dotenv.load_dotenv()


def unas_correcter_ro():
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PORT = os.environ.get("DB_PORT")
    UNAS_API = os.environ.get("UNAS_API")

    engine = create_engine('postgresql://'+DB_USER+':' +
                           DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

    column_bindings = json.loads(list(engine.execute(
        "select source_column_names from dataupload_tabletemplates where \"table\" = 'fol_unas';").fetchall()[0])[0])
    important_columns = ["Parameter_VIP_artext", "Parameter_Aremelestext", "Parameter_Belathatosagtext", "Parameter_Csaladtext", "Parameter_Csomag_kiszerelesenum", "Parameter_ELOFIZETEStext", "Parameter_Eltavolithatotext", "Parameter_Felhelyezestext", "Parameter_Felulettext", "Parameter_Hossztext", "Parameter_Hovisszaverestext", "Parameter_Illesztestext", "Parameter_Kategoriatext", "Parameter_Kiszerelesenum", "Parameter_Konzultacioenum", "Parameter_Koporetegtext", "Parameter_Lehajlo_peremtext", "Parameter_Lepesmelysegtext",
                         "Parameter_Merettext", "Parameter_Minosegtext", "Parameter_Ontapados_padloPadlotext", "Parameter_Padlo_tipusaPadlotext", "Parameter_Szelessegtext", "Parameter_Szintext", "Parameter_Teli_hangulat_mintatext", "Parameter_Tisztitasatext", "Parameter_UV_vedelemtext", "Parameter_Vastagsagtext", "Parameter_Video_segitsegVideokhtml", "Parameter_brandtext", "Parameter_m2/csomagtext", "Parameter_m2/doboztext", "Parameter_m2/tekercstext", "Parameter_1_m2_feluletheztext", "Parameter_mpntext", "Parameter_Ablakfolia_tipustext", "termek_nev", "Rovid_Leiras", "Tulajdonsagok", "Adat_1", "Adat_2", "Adat_3", "Valaszthato_Tulajdonsag_1", "Valaszthato_Tulajdonsag_2", "Valaszthato_Tulajdonsag_3", "sef_url", "Kep_ALT_TITLE", "SEO_Title", "SEO_Description", "SEO_Keywords", "SEO_Robots", "Tovabbi_lapful_cime_1", "Tovabbi_lapful_tartalma_1", "Tovabbi_lapful_cime_2", "Tovabbi_lapful_tartalma_2", "Tovabbi_lapful_cime_3", "Tovabbi_lapful_tartalma_3"]
    important_columns = [column_bindings[i] for i in important_columns]

    df = pd.read_sql(
        "select * from fol_translate where romanian != correct_romanian and is_checked_romanian = true", con=engine)
    if not df.empty:
        ids = df["original"].to_list()
        df2 = pd.DataFrame()
        for identifier in ids:
            df2 = df2.append(pd.read_sql(
                f"select * from fol_unas_translate where translation_id = '{identifier}'", con=engine))
        merged = pd.merge(df, df2, left_on="original",
                          right_on="translation_id")
        url = get_unas_feed_url(lang="hu")
        file = requests.get(url).content
        unas = pd.read_excel(file, usecols=important_columns+["Cikkszám"])
        for row in merged.iloc():
            unas.loc[unas["Cikkszám"]
                     == row["sku"], row["column"]] = row["correct_romanian"]
        unas.to_csv(
            "/home/atti/googleds/files/unas_files/romania.csv", index=False)
        token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{UNAS_API}</ApiKey></Params>'
        token_request = requests.get(
            "https://api.unas.eu/shop/login", data=token_payload)
        token_tree = ElementTree.fromstring(token_request.content)
        if token_tree[0].tag == "Token":
            global token
            token = token_tree[0].text
        romanian_url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Url>https://www.dataupload.xyz/unas_files/romania.csv</Url><DelType>no</DelType><Lang>ro</Lang></Params>'
        romanian_url_request = requests.post("https://api.unas.eu/shop/setProductDB",
                                             headers={"Authorization": f"Bearer {token}"}, data=romanian_url_payload)
        if romanian_url_request.status_code == 200:
            query = "UPDATE fol_translate SET romanian = %(correct_romanian)s WHERE original = ANY(%(originals)s)"

            # Create a list of dictionaries with the values and types
            data = [{"correct_romanian": correct, "originals": [original]}
                    for original, correct in zip(df["original"], df["correct_romanian"])]

            # Execute the query for each row in the DataFrame
            for row in data:
                engine.execute(query, row)
        print(romanian_url_request.content.decode("utf-8"))
    else:
        print("No changes")
