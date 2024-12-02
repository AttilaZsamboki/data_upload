from sqlalchemy import create_engine
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import os
from datetime import datetime

# Google Sheets API setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# SERVICE_ACCOUNT_FILE = (
#     "/home/atti/googleds/auth/pen/jutalék/dogwood-day-333815-db1f1cf5a4e8.json"
# )
SERVICE_ACCOUNT_FILE = "dogwood-day-333815-db1f1cf5a4e8.json"
SPREADSHEET_ID = "1DXOxrPHD5SA1lXHOYu3nXWWv47ArsiJOhEsVt7FUUD0"
RANGE_NAME = "RENDELÉSEK!A1"  # Starting cell where data will be inserted
FOLDER_PATH = "/path/to/your/folder"  # Replace with your actual folder path
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


def update_sheet(data_df):
    """Update Google Sheet with data"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
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

FOLDER_PATH = "../../files/fol_költségek"  # Replace with your actual folder path
FILE_SHEET_RANGE = (
    "ÖSSZES KÖLTSÉG!A1"  # New sheet name where file data will be inserted
)

# ... existing get_db_connection and query_database functions ...


def get_latest_file():
    """Get the most recent file from the specified folder"""
    files = [
        os.path.join(FOLDER_PATH, f)
        for f in os.listdir(FOLDER_PATH)
        if f.endswith(".xlsx")
    ]  # Adjust file extension if needed
    if not files:
        raise FileNotFoundError(f"No suitable files found in {FOLDER_PATH}")

    latest_file = max(files, key=os.path.getmtime)
    return latest_file


def read_file_data(file_path):
    """Read data from the latest file"""
    df = pd.read_excel(file_path)  # Adjust reading method if needed
    return df


def update_sheet2(data_df, range_name, sheet_name):
    """Updated version of update_sheet that handles different sheets"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)

    # First, get existing data
    result = (
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{sheet_name}!A1:Z",  # Expanded range to handle variable columns
        )
        .execute()
    )

    # Clear existing data in the sheet
    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{sheet_name}!A1:Z",
    ).execute()

    # Convert DataFrame to values list
    headers = data_df.columns.tolist()
    values = [headers] + data_df.values.tolist()

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
    data_df = query_database()

    # Update original sheet with database data


def main():
    # Get data from database
    data_df = query_database()

    # Update Google Sheet
    update_sheet(data_df)
    update_sheet2(data_df, FILE_SHEET_RANGE, "ÖSSZES KÖLTSÉG")


if __name__ == "__main__":
    main()
