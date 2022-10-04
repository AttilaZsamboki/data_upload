from datetime import datetime, timedelta
import pygsheets
import pandas as pd
import datetime as dt
import math
import string

# authorization
gc = pygsheets.authorize(
    service_file='/home/atti/googleds/scripts/cashflow/gs_credentials.json')

# Create empty dataframe
df = pd.DataFrame()

d1 = dt.datetime.strptime("2022.03.28", "%Y.%m.%d")
d2 = dt.datetime.strptime("2023.12.31", "%Y.%m.%d")
monday1 = (d1 - timedelta(days=d1.weekday()))
monday2 = (d2 - timedelta(days=d2.weekday()))
remaining_weeks = math.floor((monday2 - monday1).days / 7)
categories_distinct = [
    "Általános forgalmi adó (ÁFA)",
    "Egyéb szolgáltatás",
    "Szoftver költség",
    "Adó",
    "Anyagköltség",
    "Banki költség",
    "Bérjárulék",
    "Bérköltség",
    "Csomagolóanyag",
    "Egyéb",
    "Gépjármű üzemeltetés",
    "Hirdetési költség",
    "Irodai eszköz, berendezés",
    "Logisztikai szolgáltatás",
    "Magánfelhasználás",
    "Marketing költség",
    "Rendezvény",
    "Személyi jellegű ráfordítások",
    "Szoftverfejlesztés",
    "Tárgyi eszköz",
]

# Create a column
current_days_plus = 7
weeks = []
categories = []
terv = []
row = 2
alphabet = list(string.ascii_uppercase)
current_letter = "C"
for i in range(remaining_weeks):
    for j in range(len(categories_distinct)):
        weeks.append(datetime.strftime(
            d1 + dt.timedelta(days=i*7), "%Y-%m-%d"))
        categories.append(categories_distinct[j])
        terv.append(
            f"=SUMIF('ÖSSZESÍTŐ'!$B:$B; B{row};'ÖSSZESÍTŐ'!{current_letter}:{current_letter})")
        row += 1

    if len(current_letter) == 1 and current_letter != "Z":
        current_letter = alphabet[alphabet.index(current_letter)+1]
    elif current_letter == "Z":
        current_letter = "AA"
    else:
        new_letters = list(current_letter)
        if current_letter[1] != "Z":
            new_letters[1] = alphabet[alphabet.index(current_letter[1])+1]
        else:
            new_letters[0] = alphabet[alphabet.index(current_letter[0])+1]
            new_letters[1] = "A"
        current_letter = "".join(new_letters)

df["Hét"] = weeks
df["Kategória"] = categories
df["Terv"] = terv
print(df)
# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1it0dB4qCFJHCwonKdAy_vt0E-iqSA-QY6pdbmUh86E4/edit#gid=659970541')
# select the first sheet
wks = sh[0]

# update the first sheet with df, starting at cell B2.
wks.set_dataframe(df, (1, 1))
