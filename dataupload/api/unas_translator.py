import pandas as pd
from xml.etree import ElementTree
from sqlalchemy import create_engine
import requests
# import deepl
import json

DB_HOST = 'defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com'
DB_NAME = 'defaultdb'
DB_USER = 'doadmin'
DB_PASS = 'AVNS_FovmirLSFDui0KIAOnu'
DB_PORT = '25060'
AUTH_KEY = "0a74d848-fee8-1355-66b3-255562cdc6bc:fx"
UNAS_API = "de91a41477c923b33b954ac0f6d75803f5670498"

engine = create_engine('postgresql://'+DB_USER+':'+DB_PASS +
                       '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

json_data = {
    'email': 'zsamboki.attila.jr@gmail.com',
    'password': 'TznF3jY&#kp9',
}

response = requests.post(
    'https://api.translate.com/translate/v1/login', json=json_data)
token = json.loads(response.content)["data"]["token"]
headers = {
    'content-type': 'application/json',
    'authorization': f'Bearer {token}',
}


def translate_unas(file, column_bindigs):
    # Load our last stored data
    df1 = pd.read_sql_table(con=engine, table_name='fol_unas')
    df1 = df1.rename(columns=column_bindigs)
    # Get the columns where changes matter
    important_columns = ["Parameter_Felhelyezes_nehezsegetext", "Parameter_VIP_artext", "Parameter_Aremelestext", "Parameter_Belathatosagtext", "Parameter_Csaladtext", "Parameter_Csomag_kiszerelesenum", "Parameter_ELOFIZETEStext", "Parameter_Eltavolithatotext", "Parameter_Felhelyezestext", "Parameter_Felulettext", "Parameter_Hossztext", "Parameter_Hovisszaverestext", "Parameter_Illesztestext", "Parameter_Kategoriatext", "Parameter_Kiszerelesenum", "Parameter_Konzultacioenum", "Parameter_Koporetegtext", "Parameter_Lehajlo_peremtext", "Parameter_Lepesmelysegtext",
                         "Parameter_Merettext", "Parameter_Minosegtext", "Parameter_Ontapados_padloPadlotext", "Parameter_Padlo_tipusaPadlotext", "Parameter_Szelessegtext", "Parameter_Szintext", "Parameter_Teli_hangulat_mintatext", "Parameter_Tisztitasatext", "Parameter_UV_vedelemtext", "Parameter_Vastagsagtext", "Parameter_Video_segitsegVideokhtml", "Parameter_brandtext", "Parameter_m2/csomagtext", "Parameter_m2/doboztext", "Parameter_m2/tekercstext", "Parameter_1_m2_feluletheztext", "Parameter_mpntext", "Parameter_Ablakfolia_tipustext", "termek_nev", "Rovid_Leiras", "Tulajdonsagok", "Adat_1", "Adat_2", "Adat_3", "Valaszthato_Tulajdonsag_1", "Valaszthato_Tulajdonsag_2", "Valaszthato_Tulajdonsag_3", "sef_url", "Kep_ALT_TITLE", "SEO_Title", "SEO_Description", "SEO_Keywords", "SEO_Robots", "Tovabbi_lapful_cime_1", "Tovabbi_lapful_tartalma_1", "Tovabbi_lapful_cime_2", "Tovabbi_lapful_tartalma_2", "Tovabbi_lapful_cime_3", "Tovabbi_lapful_tartalma_3"]
    important_columns = [column_bindigs[i] for i in important_columns]
    # Load the live data from unas
    df2 = pd.read_excel(file)
    # Later needed dataframes for the translated data
    df2_romania = pd.read_excel(file, usecols=important_columns+["Cikkszám"])
    df2_slovakia = pd.read_excel(file, usecols=important_columns+["Cikkszám"])
    # Drop the useless column from unas's dataframe
    df2 = df2.drop(
        columns=[col for col in df2.columns if col not in df1.columns])
    df1 = df1.loc[:, ~df1.columns.duplicated()].copy()

    # Select the columns you want to compare
    merged_df = pd.merge(df1, df2, on="Cikkszám", how='inner')

    # Iterate over rows of the merged dataframe and compare values
    num_requests = 0
    for idx, row in merged_df.iterrows():
        for col in important_columns:
            df_translated = []
            df_unas = []
            # our state of the data
            x_val = row[col+'_x']
            # the newest state of the data from unas
            y_val = row[col+'_y']
            # if either is null continue
            if pd.isnull(x_val) or pd.isnull(y_val):
                continue
            # if the two data differ
            if x_val != y_val:
                romanian = []
                slovakian = []
                # check if there is already a translation for the changed unas product prop(y_val)
                db_translate = pd.read_sql_table(
                    table_name="fol_translate", con=engine)
                db_matched_rows = db_translate.loc[db_translate["original"]
                                                   == y_val]
                if not len(db_matched_rows) == 0:
                    slovakian = db_matched_rows["slovakian"].values[0]
                    romanian = db_matched_rows["romanian"].values[0]
                else:
                    json_data = {
                        'text': y_val,
                        'source_language': 'hu',
                        'translation_language': 'ro',
                    }
                    response = requests.post(
                        'https://api.translate.com/translate/v1/mt', headers=headers, json=json_data)
                    num_requests = num_requests + 1
                    if response.status_code == 200:
                        romanian = json.loads(response.content)[
                            "data"]["translation"]
                    else:
                        print(
                            f"Error in requesting a translation in col: {col}; row: {row['Cikkszám']}")
                        break

                    json_data = {
                        'text': y_val,
                        'source_language': 'hu',
                        'translation_language': 'sl',
                    }
                    response = requests.post(
                        'https://api.translate.com/translate/v1/mt', headers=headers, json=json_data)
                    num_requests = num_requests + 1
                    if response.status_code == 200:
                        slovakian = json.loads(response.content)[
                            "data"]["translation"]
                    else:
                        print(
                            f"Error in requesting a translation in col: {col}; row: {row['Cikkszám']}")
                        break
                    df_translated.append(
                        {"original": y_val, "slovakian": slovakian, "romanian": romanian, "correct_slovakian": slovakian, "correct_romanian": romanian})
                    pd.DataFrame([{"original": y_val, "slovakian": slovakian, "romanian": romanian, "correct_slovakian": slovakian, "correct_romanian": romanian}]).to_sql(
                        "fol_translate", if_exists="append", con=engine, index=False)
                df_unas.append({"translation_id": y_val, "sku":
                               row["Cikkszám"], "column": col})
                df2_romania.loc[df2_romania["Cikkszám"]
                                == row["Cikkszám"], col] = romanian
                df2_slovakia.loc[df2_slovakia["Cikkszám"]
                                 == row["Cikkszám"], col] = slovakian
                last_active_translation = engine.execute(
                    f"select translation_id from fol_unas_translate left join fol_translate on original = translation_id where sku = '{row['Cikkszám']}' and \"column\" = '{col}' and (is_checked_slovakian = false or is_checked_romanian = false)").fetchall()
                if len(last_active_translation) != 0:
                    last_active_translation = list(
                        last_active_translation[0])[0]
                    number_of_translation_uses = int(list(engine.execute(
                        f"select count(*) from fol_unas_translate where translation_id = '{y_val}'").fetchall()[0])[0])
                    engine.execute(
                        f"UPDATE fol_unas_translate SET translation_id = '{y_val}' WHERE translation_id = '{last_active_translation}' and sku = '{row['Cikkszám']}' and \"column\" = '{col}'")
                    if number_of_translation_uses == 0:
                        engine.execute(
                            f"DELETE FROM fol_translate where original = '{last_active_translation}'")
                else:
                    pd.DataFrame(df_unas).to_sql(
                        "fol_unas_translate", if_exists="append", con=engine, index=False)
    df2_romania = df2_romania[df2_romania["Cikkszám"].apply(
        lambda x: x in [i["sku"] for i in df_translated])]
    df2_romania.to_csv(
        "/home/atti/googleds/unas_files/romania.csv", index=False)
    df2_slovakia.to_csv(
        "/home/atti/googleds/unas_files/slovakia.csv", index=False)
    token_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><ApiKey>{UNAS_API}</ApiKey></Params>'
    token_request = requests.get(
        "https://api.unas.eu/shop/login", data=token_payload)
    token_tree = ElementTree.fromstring(token_request.content)
    if token_tree[0].tag == "Token":
        global token
        token = token_tree[0].text
    slovak_url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Url>https://www.dataupload.xyz/unas_files/romania.csv</Url><DelType>no</DelType><Lang>sk</Lang></Params>'
    slovak_url_request = requests.post("https://api.unas.eu/shop/setProductDB",
                                       headers={"Authorization": f"Bearer {token}"}, data=slovak_url_payload)
    roman_url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Url>https://www.dataupload.xyz/unas_files/slovakia.csv</Url><DelType>no</DelType><Lang>ro</Lang></Params>'
    roman_url_request = requests.post("https://api.unas.eu/shop/setProductDB",
                                      headers={"Authorization": f"Bearer {token}"}, data=roman_url_payload)
    print(num_requests)
