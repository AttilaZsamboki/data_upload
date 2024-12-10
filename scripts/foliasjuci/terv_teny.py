from sqlalchemy import create_engine
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import os
from datetime import datetime
import base64
import json
from dotenv import load_dotenv

load_dotenv()

# Google Sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SERVICE_ACCOUNT_FILE = (
#     "/home/atti/googleds/auth/pen/jutalék/dogwood-day-333815-db1f1cf5a4e8.json"
# )
SERVICE_ACCOUNT_FILE = "dogwood-day-333815-db1f1cf5a4e8.json"
SPREADSHEET_ID = "1DXOxrPHD5SA1lXHOYu3nXWWv47ArsiJOhEsVt7FUUD0"
RANGE_NAME = "RENDELÉSEK!A1"  # Starting cell where data will be inserted
FILE_SHEET_RANGE = "TERVEK!A1"  # New sheet name where file data will be inserted


def get_db_connection():
    """Create database connection"""
    # Replace with your database connection string
    DB_HOST = "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com"
    DB_NAME = "defaultdb"
    DB_USER = "doadmin"
    DB_PASS = "AVNS_FovmirLSFDui0KIAOnu"
    DB_PORT = "25060"
    engine = create_engine(
        "postgresql://"
        + DB_USER
        + ":"
        + DB_PASS
        + "@"
        + DB_HOST
        + ":"
        + DB_PORT
        + "/"
        + DB_NAME
    )

    return engine


def query_database():
    """Query data from database"""
    engine = get_db_connection()

    # Query to get current month's totals
    query = """
    SELECT 
        DATE_TRUNC('month', CURRENT_DATE) as "Hónap",
        SUM("Cogs") as "Cogs",
        SUM("Order_Total") as "Total"
    FROM fol_orders
    WHERE DATE_TRUNC('month', "Order_Date") = DATE_TRUNC('month', CURRENT_DATE) and "Order_Status" = 'Completed' and "Row_Type" = 'Order'
    GROUP BY DATE_TRUNC('month', CURRENT_DATE)
    """

    df = pd.read_sql(query, engine)
    return df


def get_credentials():
    """Get credentials from environment variable"""
    # Get base64 encoded credentials from environment
    encoded_creds = os.environ.get("GOOGLE_CREDENTIALS")
    if not encoded_creds:
        raise ValueError("GOOGLE_CREDENTIALS environment variable not set")

    # Decode and create temp file
    creds_json = base64.b64decode(encoded_creds)
    credentials = service_account.Credentials.from_service_account_info(
        json.loads(creds_json), scopes=SCOPES
    )
    return credentials


def update_sheet_orders():
    data_df = query_database()
    """Update Google Sheet with data"""
    credentials = get_credentials()
    service = build("sheets", "v4", credentials=credentials)

    # First, get existing data
    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range="RENDELÉSEK!A1:C",  # Get all rows for our three columns
        )
        .execute()
    )

    existing_values = result.get("values", [])
    if not existing_values:
        existing_values = [["Hónap", "Cogs", "Total"]]  # Headers if sheet is empty

    # Convert existing data to DataFrame
    existing_df = pd.DataFrame(existing_values[1:], columns=existing_values[0])
    if not existing_df.empty:
        existing_df["Hónap"] = pd.to_datetime(existing_df["Hónap"])

    # Get current month's data
    current_month = data_df["Hónap"].iloc[0].strftime("%Y-%m-%d")

    # Check if month exists
    if not existing_df.empty and (existing_df["Hónap"] == current_month).any():
        # Update existing row
        row_idx = (
            existing_df.index[existing_df["Hónap"] == current_month][0] + 2
        )  # +2 for 1-based index and header
        range_name = f"RENDELÉSEK!A{row_idx}:C{row_idx}"
    else:
        # Append new row
        range_name = (
            f"RENDELÉSEK!A{len(existing_values) + 1}:C{len(existing_values) + 1}"
        )

    # Prepare values for update
    values = [
        [
            data_df["Hónap"].iloc[0].strftime("%Y-%m-%d"),
            round(float(data_df["Cogs"].iloc[0]), 0),
            round(float(data_df["Total"].iloc[0]), 0),
        ]
    ]

    body = {"values": values}

    # Update the sheet
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )

    # ... existing imports ...


import os

FILE_SHEET_RANGE = (
    "ÖSSZES KÖLTSÉG!A1"  # New sheet name where file data will be inserted
)


def update_sheet_expenses(range_name, sheet_name):
    """Updated version of update_sheet that handles different sheets"""
    engine = get_db_connection()
    data_df = pd.read_sql(
        """select date "Dátum", 
                  to_char(date, 'YYYY-MM') "Hónap", 
                  koltseg_osztaly "Költség osztály", 
                  koltsegelem "Költségelem", 
                  partner "Partner", 
                  tipus "Költség típus", 
                  ROUND(CAST(netto_ossz AS numeric), 0)::integer "NETTÓ Összesen" 
           from "fol_költségek_extended";""",
        engine,
    )

    # Replace NaN values with None (null)
    data_df = data_df.where(pd.notnull(data_df), None)

    credentials = get_credentials()
    service = build("sheets", "v4", credentials=credentials)

    # Clear existing data in the sheet
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1:Z",
    ).execute()

    # Convert DataFrame to values list
    headers = data_df.columns.tolist()
    values = [headers]

    # Convert each row, handling dates and other special values
    for _, row in data_df.iterrows():
        formatted_row = []
        for val in row:
            if pd.isna(val):
                formatted_row.append(None)
            elif isinstance(val, (datetime, pd.Timestamp)) or hasattr(val, "strftime"):
                formatted_row.append(val.strftime("%Y-%m-%d"))
            else:
                formatted_row.append(val)
        values.append(formatted_row)

    body = {"values": values}

    # Update the sheet
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        )
        .execute()
    )

    print(f"{result.get('updatedCells')} cells updated in {sheet_name}.")


def main():
    # Get data from database

    # Update Google Sheet
    update_sheet_orders()
    update_sheet_expenses(FILE_SHEET_RANGE, "ÖSSZES KÖLTSÉG")


if __name__ == "__main__":
    main()
