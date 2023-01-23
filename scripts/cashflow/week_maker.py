from datetime import datetime, timedelta
import pygsheets
import pandas as pd
import datetime as dt
import math
import string
from dateutil.relativedelta import relativedelta

# authorization
gc = pygsheets.authorize(
    service_file='/home/atti/googleds/scripts/cashflow/gs_credentials.json')

# Create empty dataframe
df = pd.DataFrame()

starting_date = input("Starting date: ")
end_date = input("End date: ")
d1 = dt.datetime.strptime(starting_date, "%Y.%m.%d")
d2 = dt.datetime.strptime(end_date, "%Y.%m.%d")
monday1 = (d1 - timedelta(days=d1.weekday()))
monday2 = (d2 - timedelta(days=d2.weekday()))
remaining_weeks = math.floor((monday2 - monday1).days / 7)
categories_distinct = [
    'Albérlet kiadás',
    'Bónusz jóváírás',
    'Csomagautomata bérbeadás',
    'Csomagplusz jutalék',
    'Értékesítés',
    'GINOP',
    'Kaució',
    'Packeta jutalék',
    'Beszállító jóváírás',
    'Szoftver értékesítés',
    'Oktatás értékesítés',
]


# Create a column
current_days_plus = 7
weeks = []
categories = []
terv = []
row = 2
interval = input("Interval (M/D): ")
alphabet = list(string.ascii_uppercase)
current_letter = input("What is the starting letter? ")
main_table = input("What is the name of the source table? ")
plan_table_check_col = input("Which column should it compare to? ")
for i in range(remaining_weeks):
    for j in range(len(categories_distinct)):
        if interval == "D":
            weeks.append(datetime.strftime(
                d1 + dt.timedelta(days=i), "%Y-%m-%d"))
        elif interval == "M":
            weeks.append(datetime.strftime(
                d1 + relativedelta(months=+i), "%Y-%m-%d"))
        categories.append(categories_distinct[j])
        terv.append(
            f"=SUMIF('{main_table}'!${plan_table_check_col}:${plan_table_check_col}; B{row};'{main_table}'!{current_letter}:{current_letter})")
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
url = input("Mi az url? ")
sh = gc.open_by_url(
    url)
# select the first sheet
wks = sh[0]

# update the first sheet with df, starting at cell B2.
wks.set_dataframe(df, (1, 1))
