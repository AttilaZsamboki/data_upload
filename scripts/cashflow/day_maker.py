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

d1 = dt.datetime.strptime("2022.11.28", "%Y.%m.%d")
d2 = dt.datetime.strptime("2023.11.28", "%Y.%m.%d")
remaining_days = math.floor((d2 - d1).days)
categories_distinct = [
    "Egyéb szolgáltatás",
    "Szoftver költség",
    "Általános forgalmi adó (ÁFA)",
    "Adó",
    "Anyagköltség",
    "Banki költség",
    "Bérjárulék",
    "Bérköltség",
    "Csomagolóanyag",
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
    "Egyéb",
]

# Create a column
current_days_plus = 1
weeks = []
categories = []
terv = []
row = 2
alphabet = list(string.ascii_uppercase)
current_letter = "C"
for i in range(remaining_days):
    for j in range(len(categories_distinct)):
        weeks.append(datetime.strftime(
            d1 + dt.timedelta(days=i), "%Y-%m-%d"))
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

df["Nap"] = weeks
df["Kategória"] = categories
df["Terv"] = terv
print(df)
# open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open_by_url(
    'https://docs.google.com/spreadsheets/d/1jnpNene2e9Yh4lWNx9uPNQCOCgWgYjQrIX_DRTKpxGE/edit#gid=503639935')
# select the first sheet
wks = sh[0]

# update the first sheet with df, starting at cell B2.
wks.set_dataframe(df, (1, 1))
