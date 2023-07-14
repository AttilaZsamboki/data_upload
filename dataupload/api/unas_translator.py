import pandas as pd
from xml.etree import ElementTree
from sqlalchemy import create_engine, text
import requests
import deepl
import os
import dotenv
dotenv.load_dotenv()


def translate_unas(file, column_bindigs):
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PORT = os.environ.get("DB_PORT")
    AUTH_KEY = "0a74d848-fee8-1355-66b3-255562cdc6bc:fx"
    UNAS_API = os.environ.get("UNAS_API")

    engine = create_engine('postgresql://'+DB_USER+':'+DB_PASS +
                           '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)
    translator = deepl.Translator(AUTH_KEY)
    # Load our last stored data
    df1 = pd.read_sql_table(con=engine, table_name='fol_unas')
    df1 = df1.rename(columns=column_bindigs)
    # Get the columns where changes matter
    important_columns = ["Parameter_VIP_artext", "Parameter_Aremelestext", "Parameter_Belathatosagtext", "Parameter_Csaladtext", "Parameter_Csomag_kiszerelesenum", "Parameter_ELOFIZETEStext", "Parameter_Eltavolithatotext", "Parameter_Felhelyezestext", "Parameter_Felulettext", "Parameter_Hossztext", "Parameter_Hovisszaverestext", "Parameter_Illesztestext", "Parameter_Kategoriatext", "Parameter_Kiszerelesenum", "Parameter_Konzultacioenum", "Parameter_Koporetegtext", "Parameter_Lehajlo_peremtext", "Parameter_Lepesmelysegtext",
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
    if df1.empty:
        df1["Cikkszám"] = df2["Cikkszám"]
    elif len(df1) < len(df2):
        # Get the key column from both DataFrames
        key_col_1 = df1["Cikkszám"]
        key_col_2 = df2["Cikkszám"]

        # Get a boolean mask for the values in key_col_2 that are not in key_col_1
        mask = ~key_col_2.isin(key_col_1)

        # Use the mask to filter the rows from df2 that you want to append to df1
        append_rows = df2[mask]
        for col in append_rows.columns:
            if col != "Cikkszám":
                append_rows[col] = ""
        # Append the filtered rows to df1
        df1 = df1.append(append_rows)

    merged_df = pd.merge(df1, df2, on="Cikkszám", how='inner')

    # Iterate over rows of the merged dataframe and compare values
    num_requests = 0
    df_translated = []
    for idx, row in merged_df.iterrows():
        for col in important_columns:
            df_unas = []
            # our state of the data
            x_val = row[col+'_x']
            # the newest state of the data from unas
            y_val = row[col+'_y']
            # if either is null continue
            if pd.isnull(y_val):
                continue
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
                    romanian = translator.translate_text(
                        y_val, target_lang="RO", tag_handling="html").text
                    slovakian = translator.translate_text(
                        y_val, target_lang="SK", tag_handling="html").text
                    num_requests += 2
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
                    query = text(
                        "select count(*) from fol_unas_translate where translation_id = :translation_id")
                    number_of_translation_uses = engine.execute(
                        query, translation_id=y_val).scalar()
                    query = text(
                        "UPDATE fol_unas_translate SET translation_id = :y_val WHERE translation_id = :last_active_translation and sku = :sku and \"column\" = :col")
                    engine.execute(
                        query, y_val=y_val, last_active_translation=last_active_translation, sku=row["Cikkszám"], col=col)
                    if number_of_translation_uses == 0:
                        engine.execute(
                            f"DELETE FROM fol_translate where original = '{last_active_translation}'")
                else:
                    pd.DataFrame(df_unas).to_sql(
                        "fol_unas_translate", if_exists="append", con=engine, index=False)
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
    slovak_url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Url>https://www.dataupload.xyz/unas_files/slovakia.csv</Url><DelType>no</DelType><Lang>sk</Lang></Params>'
    slovak_url_request = requests.post("https://api.unas.eu/shop/setProductDB",
                                       headers={"Authorization": f"Bearer {token}"}, data=slovak_url_payload)
    roman_url_payload = f'<?xml version="1.0" encoding="UTF-8" ?><Params><Url>https://www.dataupload.xyz/unas_files/romania.csv</Url><DelType>no</DelType><Lang>ro</Lang></Params>'
    roman_url_request = requests.post("https://api.unas.eu/shop/setProductDB",
                                      headers={"Authorization": f"Bearer {token}"}, data=roman_url_payload)
    print("Num requests: ", num_requests)


# url = get_unas_feed_url()
# file = requests.get(url).content
# print(translate_unas(file=file, column_bindigs={"Parameter_Video_segitsegVideokhtml": "Paraméter: Videó segítség|Videók|html|1|0|0|0|0|0|||0|1|1", "Parameter_Csomag_kiszerelesenum": "Paraméter: Csomag kiszerelés||enum|1|0|0|0|0|0|||0|1|1", "Parameter_Vastagsagtext": "Paraméter: Vastagság||text|1|0|1|0|0|0|||0|1|1", "Parameter_Hovisszaverestext": "Paraméter: Hővisszaverés||text|1|0|1|0|0|0|||0|1|1", "termek_nev": "Termék Név", "Parameter_Felhelyezestext": "Paraméter: Felhelyezés||text|1|0|1|1|0|0|||0|1|1", "Parameter_Illesztestext": "Paraméter: Illesztés||text|1|0|1|0|0|0|||0|1|1", "Parameter_Teli_hangulat_mintatext": "Paraméter: Téli hangulat minta||text|1|0|1|0|1|0|||0|1|1", "Parameter_Csaladtext": "Paraméter: Család||text|1|0|0|1|0|0|||0|1|1", "Parameter_m2/csomagtext": "Paraméter: m2/csomag||text|1|0|1|0|0|0|||0|1|1", "Parameter_Eltavolithatotext": "Paraméter: Eltávolítható||text|1|0|1|0|0|0|||0|1|1", "Parameter_Belathatosagtext": "Paraméter: Beláthatóság||text|1|0|1|0|0|0|||0|1|1", "Parameter_Kategoriatext": "Paraméter: Kategória||text|0|1|1|0|0|0|||0|1|0", "Parameter_Koporetegtext": "Paraméter: Kopóréteg||text|1|0|1|0|0|0|||0|1|1", "Parameter_Szelessegtext": "Paraméter: Szélesség||text|2|0|1|1|0|0|||0|1|1", "Parameter_mpntext": "Paraméter: mpn||text|0|0|0|0|0|0|||0|1|1", "Parameter_Merettext": "Paraméter: Méret||text|2|0|1|1|1|0|||0|1|1", "Parameter_brandtext": "Paraméter: brand||text|0|0|0|0|0|0|||0|1|1", "Parameter_UV_vedelemtext": "Paraméter: UV védelem||text|1|0|1|0|0|0|||0|1|1", "Parameter_Felhelyezes_nehezsegetext": "Paraméter: Felhelyezés nehézsége||text|1|0|1|0|0|0|||0|1|1", "id": "", "Parameter_Konzultacioenum": "Paraméter: Konzultáció||enum|1|0|1|0|1|0|||0|1|1", "Parameter_Felulettext": "Paraméter: 1 m2 felülethez||text|2|0|1|0|0|0|||0|1|1", "Parameter_m2/tekercstext": "Paraméter: m2/tekercs||text|2|0|1|0|0|0|||0|1|1", "Parameter_VIP_artext": "Paraméter: VIP ár||text|0|0|1|0|0|0|||0|1|0",
#                                                 "Parameter_Szintext": "Paraméter: Szín||text|1|0|1|1|0|0|||0|1|1", "Parameter_Lepesmelysegtext": "Paraméter: Lépésmélység||text|1|0|1|0|0|0|||0|1|1", "Parameter_Minosegtext": "Paraméter: Minőség||text|2|1|0|1|0|0|||0|1|0", "Parameter_m2/doboztext": "Paraméter: m2/doboz||text|2|0|1|0|0|0|||0|1|1", "Parameter_Lehajlo_peremtext": "Paraméter: Lehajló perem||text|1|0|1|0|0|0|||0|1|1", "Parameter_Ontapados_padloPadlotext": "Paraméter: Öntapadós padló|Padló|text|1|0|1|0|0|0|||0|1|1", "cikkszam": "Cikkszám", "Parameter_Padlo_tipusaPadlotext": "Paraméter: Padló típusa|Padló|text|1|0|1|0|0|0|||0|1|1", "Category": "Kategória", "brutto_ar": "Bruttó Ár", "Parameter_ELOFIZETEStext": "Paraméter: ELŐFIZETÉS||text|1|0|1|0|0|0|||0|1|1", "Parameter_Ablakfolia_tipustext": "Paraméter: Ablakfólia típus||text|1|0|1|0|0|0|||0|1|1", "Parameter_Kiszerelesenum": "Paraméter: Kiszerelés||enum|2|0|0|0|1|0|||0|1|1", "Parameter_Tisztitasatext": "Paraméter: Tisztítása||text|1|0|1|0|0|0|||0|1|1", "Parameter_Hossztext": "Paraméter: Hossz||text|2|0|1|1|0|0|||0|1|1", "netto_ar": "Nettó Ár", "Parameter_Aremelestext": "Paraméter: Áremelés||text|0|0|0|0|0|0|||0|1|0", "Rovid_Leiras": "Rövid Leírás", "Tulajdonsagok": "Tulajdonságok", "Adat_1": "Adat 1", "Adat_2": "Adat 2", "Adat_3": "Adat 3", "Valaszthato_Tulajdonsag_1": "Választható Tulajdonság 1", "Valaszthato_Tulajdonsag_2": "Választható Tulajdonság 2", "Valaszthato_Tulajdonsag_3": "Választható Tulajdonság 3", "sef_url": "SEF URL", "Kep_ALT_TITLE": "Kép ALT/TITLE", "SEO_Title": "SEO Title", "SEO_Description": "SEO Description", "SEO_Keywords": "SEO Keywords", "SEO_Robots": "SEO Robots", "Tovabbi_lapful_cime_1": "További lapfül címe 1", "Tovabbi_lapful_tartalma_1": "További lapfül tartalma 1", "Tovabbi_lapful_cime_2": "További lapfül címe 2", "Tovabbi_lapful_tartalma_2": "További lapfül tartalma 2", "Tovabbi_lapful_cime_3": "További lapfül címe 3", "Tovabbi_lapful_tartalma_3": "További lapfül tartalma 3", "Parameter_1_m2_feluletheztext": "Paraméter: 1 m2 felülethez||text|2|0|1|0|0|0|||0|1|1"}))
