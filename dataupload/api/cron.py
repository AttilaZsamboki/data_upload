import datetime
from google.oauth2 import service_account
import requests
import json
import pandas as pd
from datetime import date
from googleapiclient.discovery import build
import logging
from base64 import urlsafe_b64decode
import os
import json
from .models import DatauploadUploadmodel, DatauploadTabletemplates, Feed, DatauploadGroups, DatauploadTableOverview, SMVendorOrders
from .upload_handler import handle_uploaded_file
import requests
from datetime import date, datetime, timedelta
from .utils.gmail import gmail_authenticate, send_email
import requests
import pandas as pd
from sqlalchemy import create_engine
from .unas_translator import translate_unas
from .unas_translator_correcter_ro import unas_correcter_ro
from .unas_translator_correcter_sk import unas_correcter_sk
from .utils.unas_feed import get_unas_feed_url
from .utils.unas_img import get_unas_img_feed_url
from .sm.inventory_planner import inventory_planner
from .sm.fetch_data import sm_fetch_data
from .utils.logs import log


def upload_file():
    for upload in DatauploadUploadmodel.objects.all():
        table, file, is_new_table, status = (
            upload.table, upload.file, upload.is_new_table, upload.status)
        if status == "ready":
            if not is_new_table:
                table_template = DatauploadTabletemplates.objects.get(
                    table=table)
                try:
                    column_bindings = json.loads(
                        table_template.source_column_names)
                except:
                    print("Json convert error")
            else:
                table_template = {}
                column_bindings = {}
            handle_uploaded_file(file, table,
                                 table_template, upload.user_id, is_new_table, column_bindings, False)


def upload_feed_daily():
    current_hour = (datetime.now() + timedelta(hours=2)).hour
    for upload in Feed.objects.filter(runs_at=current_hour):
        table, url, user_id, frequency = (
            upload.table, upload.url, upload.user_id, upload.frequency)
        if frequency == "1 nap":
            log(f"Feed '{table}' feltöltése elkezdődött",
                "INFO", "upload_feed_daily")
            if table == "fol_unas":
                url = get_unas_feed_url()
            try:
                file = requests.get(url).content
            except:
                print("Not valid url for file")
                log(f"Feed '{table}' nem érhető el a megadott url-en({url})",
                    "ERROR", "upload_feed_daily")
                continue
            files_already_existing = [f for f in os.listdir(
                f"/home/atti/googleds/files/{table}/") if f"{date.today()}" in f]
            filename = f"/home/atti/googleds/files/{table}/{date.today()}{f' ({len(files_already_existing)})' if files_already_existing else ''}.xlsx"
            try:
                open(filename, "wb").write(file)
            except:
                log(f"Feed '{table}' nem érhető el a megadott url-en({url})",
                    "ERROR", "upload_feed_daily")
            uploadmodel = DatauploadUploadmodel(
                table=table, file=filename, user_id=user_id, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
            uploadmodel.save()
            table_template = DatauploadTabletemplates.objects.get(
                table=table)
            try:
                column_bindings = json.loads(
                    table_template.source_column_names)
            except:
                print("Json convert error")
            try:
                handle_uploaded_file(filename, table,
                                     table_template, user_id, False, column_bindings, True)
            except ValueError:
                uploadmodel.table = table
                uploadmodel.status = "error"
                uploadmodel.status_description = "Hibás fájl tartalom"
                uploadmodel.save()
                log("Hibás fájl tartalom", "FAILED", "upload_feed_daily")
                print("Could not upload file")
                continue
            except:
                uploadmodel.table = table
                uploadmodel.status = "error"
                uploadmodel.status_description = "Hiba történt a fájl feltöltése közben."
                uploadmodel.save()
                log(f"Hiba történt a fájl feltöltése közben. \n Tábla {table} \n URL {url} \n User {user_id}",
                    "ERROR", "upload_feed_daily")
                continue


def upload_feed_weekly():
    for upload in Feed.objects.all():
        table, url, user_id, frequency = (
            upload.table, upload.url, upload.user_id, upload.frequency)
        if frequency == "1 hét":
            try:
                file = requests.get(url).content
            except:
                print("Not valid url for file")
                continue
            files_already_existing = [f for f in os.listdir(
                f"/home/atti/googleds/files/{table}/") if f"{date.today()}" in f]
            filename = f"/home/atti/googleds/files/{table}/{date.today()}{f' ({len(files_already_existing)})' if files_already_existing else ''}.xlsx"
            open(filename, "wb").write(file)
            uploadmodel = DatauploadUploadmodel(
                table=table, file=filename, user_id=user_id, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
            uploadmodel.save()
            table_template = DatauploadTabletemplates.objects.get(
                table=table)
            try:
                column_bindings = json.loads(
                    table_template.source_column_names)
            except:
                print("Json convert error")
            try:
                handle_uploaded_file(filename, table,
                                     table_template, user_id, False, column_bindings, True)
            except ValueError:
                uploadmodel.table = table
                uploadmodel.status = "error"
                uploadmodel.status_description = "Hibás fájl tartalom"
                uploadmodel.save()
                print("Could not upload file")
                continue


def upload_feed_hourly():
    for upload in Feed.objects.all():
        table, url, user_id, frequency = (
            upload.table, upload.url, upload.user_id, upload.frequency)
        if frequency == "1 óra":
            try:
                file = requests.get(url).content
            except:
                print("Not valid url for file")
                continue
            files_already_existing = [f for f in os.listdir(
                f"/home/atti/googleds/files/{table}/") if f"{date.today()}" in f]
            filename = f"/home/atti/googleds/files/{table}/{date.today()}{f' ({len(files_already_existing)})' if files_already_existing else ''}.xlsx"
            open(filename, "wb").write(file)
            uploadmodel = DatauploadUploadmodel(
                table=table, file=filename, user_id=user_id, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
            uploadmodel.save()
            table_template = DatauploadTabletemplates.objects.get(
                table=table)
            try:
                column_bindings = json.loads(
                    table_template.source_column_names)
            except:
                print("Json convert error")
            try:
                handle_uploaded_file(filename, table,
                                     table_template, user_id, False, column_bindings, True)
            except ValueError:
                uploadmodel.table = table
                uploadmodel.status = "error"
                uploadmodel.status_description = "Hibás fájl tartalom"
                uploadmodel.save()
                print("Could not upload file")
                continue


def email_uploads():

    def search_messages(service, query):
        result = service.users().messages().list(userId='me', q=query).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(
                userId='me', q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    # utility functions

    def get_size_format(b, factor=1024, suffix="B"):
        """
        Scale bytes to its proper byte format
        e.g:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
            if b < factor:
                return f"{b:.2f}{unit}{suffix}"
            b /= factor
        return f"{b:.2f}Y{suffix}"

    def clean(text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)

    def parse_parts(service, parts, folder_name, message, sender_email):
        """
        Utility function that parses the content of an email partition
        """
        if parts:
            for part in parts:
                filename = part.get("filename")
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")
                file_size = body.get("size")
                part_headers = part.get("headers")
                if part.get("parts"):
                    # recursively call this function when we see that a part
                    # has parts inside
                    parse_parts(service, part.get("parts"),
                                folder_name, message, sender_email)

                if mimeType == "text/plain":
                    # if the email part is text plain
                    if data:
                        global text
                        text = urlsafe_b64decode(data).decode()
                        print(text)
                else:
                    # attachment other than a plain text or HTML
                    for part_header in part_headers:
                        part_header_name = part_header.get("name")
                        part_header_value = part_header.get("value")
                        if part_header_name == "Content-Disposition":
                            if "attachment" in part_header_value:
                                # we get the attachment ID
                                # and make another request to get the attachment itself
                                print("Saving the file:", filename,
                                      "size:", get_size_format(file_size))
                                attachment_id = body.get("attachmentId")
                                attachment = service.users().messages() \
                                    .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                                data = attachment.get("data")
                                if data:
                                    headers = {
                                        'Accept': '*/*',
                                        # Already added when you pass json=
                                        # 'Content-Type': 'application/json',
                                        'Authorization': 'Bearer uf_live_admin_6nz455rn_9174142975ec131dcc59fa0b55977be2',
                                    }
                                    response = requests.post(
                                        'https://api.userfront.com/v0/users/find', headers=headers)
                                    sender_email = sender_email.replace(
                                        "<", "").replace(">", "")
                                    user = [i for i in json.loads(response.content)[
                                        "results"] if i["email"] == sender_email][0]
                                    user_id = user["userId"]
                                    groups = DatauploadGroups.objects.filter(
                                        user_ids__contains=user_id)
                                    if len(groups) > 1:
                                        if text:
                                            group = [
                                                i for i in groups if i.group == text.replace("\r\n", "")][0]
                                    else:
                                        group = groups[0]
                                    tables = [i.email_name for i in DatauploadTableOverview.objects.filter(available_at__contains="upload"
                                                                                                           ) if i.db_table in group.tables and i.email_name in filename]
                                    table = ""
                                    for i in tables:
                                        table = DatauploadTableOverview.objects.get(
                                            email_name=i, group=group.group).db_table
                                    if table == "":
                                        send_email(service, sender_email, "Feltöltés hiba",
                                                   f"'{filename}' nem megfelelő fájlnév, tartalmaznia kell egy tábla nevét az aláábiak közül: {', '.join([i[4:] for i in tables])}", [])
                                    filename, extension_format = os.path.splitext(
                                        str(filename))
                                    file_number = len([f for f in os.listdir(
                                        f'{folder_name}{table}') if filename in f])
                                    filename = f"{filename}{f' ({file_number})' if file_number else ''}{extension_format}"
                                    filepath = f"{folder_name}{table}/{filename}"
                                    table_template = DatauploadTabletemplates.objects.get(
                                        table=table)
                                    column_bindings = json.loads(
                                        table_template.source_column_names)
                                    with open(filepath, "wb") as f:
                                        f.write(urlsafe_b64decode(data))
                                    uploadmodel = DatauploadUploadmodel(table=table, file=filepath, user_id=user_id, is_new_table=False,
                                                                        upload_timestamp=datetime.now(), mode="Email", status="ready")
                                    uploadmodel.save()
                                    handle_uploaded_file(file=filepath, table=table,
                                                         table_template=table_template, user_id=user_id, is_new_table=False, column_bindings=column_bindings, is_feed=False, is_email=True, sender_email=sender_email)

    def read_message(service, message):
        """
        This function takes Gmail API `service` and the given `message_id` and does the following:
            - Downloads the content of the email
            - Prints email basic information (To, From, Subject & Date) and plain/text parts
            - Creates a folder for each email based on the subject
            - Downloads text/html content (if available) and saves it under the folder created as index.html
            - Downloads any file that is attached to the email and saves it in the folder created
        """
        msg = service.users().messages().get(
            userId='me', id=message['id'], format='full').execute()
        # parts can be the message body, or attachments
        payload = msg['payload']
        headers = payload.get("headers")
        parts = payload.get("parts")
        folder_name = "email"
        sender_email = ""
        if headers:
            # this section prints email basic info & creates a folder for the email
            for header in headers:
                name = header.get("name")
                value = header.get("value")
                if name.lower() == 'from':
                    # we print the From address
                    print("From:", value)
                if name.lower() == "return-path":
                    sender_email = value
                if name.lower() == "to":
                    # we print the To address
                    print("To:", value)
                if name.lower() == "subject":
                    # make our boolean True, the email has "subject"
                    has_subject = True
                    # make a directory with the name of the subject
                    folder_name = clean(value)
                    # we will also handle emails with the same subject name
                    folder_counter = 0
                    while os.path.isdir(folder_name):
                        folder_counter += 1
                        # we have the same folder name, add a number next to it
                        if folder_name[-1].isdigit() and folder_name[-2] == "_":
                            folder_name = f"{folder_name[:-2]}_{folder_counter}"
                        elif folder_name[-2:].isdigit() and folder_name[-3] == "_":
                            folder_name = f"{folder_name[:-3]}_{folder_counter}"
                        else:
                            folder_name = f"{folder_name}_{folder_counter}"
                    print("Subject:", value)
                if name.lower() == "date":
                    # we print the date when the message was sent
                    print("Date:", value)
        parse_parts(service, parts,
                    "/home/atti/googleds/files/", message, sender_email)
        print("="*50)

    def delete_messages(service, query):
        messages_to_delete = search_messages(service, query)
        # it's possible to delete a single message with the delete API, like this:
        # service.users().messages().delete(userId='me', id=msg['id'])
        # but it's also possible to delete all the selected messages with one query, batchDelete
        return service.users().messages().batchDelete(
            userId='me',
            body={
                'ids': [msg['id'] for msg in messages_to_delete]
            }
        ).execute()

    service = gmail_authenticate("sajat")

    results = search_messages(service, "Feltöltés")
    print(f"Found {len(results)} results.")

    for msg in results:
        read_message(service, msg)
    delete_messages(service, "Feltöltés")


def upload_pro_stock_month():
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PORT = os.environ.get("DB_PORT")
    engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                           "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"")
    for upload in Feed.objects.all():
        table, url, user_id, frequency = (
            upload.table, upload.url, upload.user_id, upload.frequency)
        if table == "pro_stock_report":
            result = engine.execute(
                "select case when max(timestamp)::date = current_date then false else true end from pro_stock_report")
            if (result.fetchone()[0]):
                try:
                    file = requests.get(url).content
                except:
                    print("Not valid url for file")
                    continue
                files_already_existing = [f for f in os.listdir(
                    f"/home/atti/googleds/files/{table}/") if f"{date.today()}" in f]
                filename = f"/home/atti/googleds/files/{table}/{date.today()}{f' ({len(files_already_existing)})' if files_already_existing else ''}.xlsx"
                open(filename, "wb").write(file)
                uploadmodel = DatauploadUploadmodel(
                    table=table, file=filename, user_id=user_id, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
                uploadmodel.save()
                table_template = DatauploadTabletemplates.objects.get(
                    table=table)
                try:
                    column_bindings = json.loads(
                        table_template.source_column_names)
                except:
                    print("Json convert error")
                try:
                    handle_uploaded_file(filename, table,
                                         table_template, user_id, False, column_bindings, True)
                except ValueError:
                    uploadmodel.table = table
                    uploadmodel.status = "error"
                    uploadmodel.status_description = "Hibás fájl tartalom"
                    uploadmodel.save()
                    print("Could not upload file")
                    continue
            else:
                print("NOT TODAY")


def pro_stock_report_summary():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PORT = os.environ.get("DB_PORT")

    engine = create_engine("postgresql://"+DB_USER+":"+DB_PASS +
                           "@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME+"")

    df = pd.read_sql("""
        WITH min_funnel AS (SELECT pro_stock_report_extended."timestamp",
                           count(DISTINCT pro_stock_report_extended."SKU")        AS min_sku,
                           sum(pro_stock_report_extended."Inventory_Value_Layer") AS min_stock_value
                    FROM pro_stock_report pro_stock_report_extended
                             LEFT JOIN pro_products pp ON pro_stock_report_extended."SKU" = pp."SKU"
                             LEFT JOIN pro_product_suppliers pps ON pro_stock_report_extended."SKU" = pps."SKU"
                    WHERE pp."Minimum_Stock_Quantity" > 0::double precision
                      AND pp."Minimum_Stock_Quantity" IS NOT NULL
                      AND pro_stock_report_extended."Layers_Warehouse" IS NOT NULL
                      AND pro_stock_report_extended."SKU" !~~ 'TE_%%'::text
                    GROUP BY pro_stock_report_extended."timestamp"),
     funnel AS (SELECT pro_stock_report_extended."timestamp",
                       sum(pro_stock_report_extended."Minimum_Stock_Quantity") AS min_stock,
                       sum(pro_stock_report_extended."Inventory_Value_Layer")  AS net_stock_value,
                       sum(pro_stock_report_extended."On_Stock_Layer")         AS quantity,
                       count(DISTINCT pro_stock_report_extended."SKU")         AS skus
                FROM pro_stock_report_extended
                         LEFT JOIN pro_product_suppliers pps ON pro_stock_report_extended."SKU" = pps."SKU"
                WHERE pro_stock_report_extended."Layers_Warehouse" IS NOT NULL
                  AND pro_stock_report_extended."SKU" !~~ 'TE_%%'::text
                GROUP BY pro_stock_report_extended."timestamp")
    SELECT f."timestamp" as month,
        f.net_stock_value,
        f.quantity,
        f.skus,
        mf.min_stock_value,
        f.min_stock,
        mf.min_sku
    FROM funnel f
            LEFT JOIN min_funnel mf ON mf."timestamp" = f."timestamp"
    WHERE f.timestamp = '2023-07-01'
    """, con=engine)
    df.to_sql("pro_stock_report_summary", con=engine,
              index=False, if_exists="append")


def unas_upload_and_translate():
    ## -- Uplaod -- ##
    url = get_unas_feed_url()
    table = "fol_unas"
    try:
        file = requests.get(url).content
    except:
        print("Not valid url for file")
        return
    files_already_existing = [f for f in os.listdir(
        f"/home/atti/googleds/files/{table}/") if f"{date.today()}" in f]
    filename = f"/home/atti/googleds/files/{table}/{date.today()}{f' ({len(files_already_existing)})' if files_already_existing else ''}.xlsx"
    open(filename, "wb").write(file)
    uploadmodel = DatauploadUploadmodel(
        table=table, file=filename, user_id=1, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
    uploadmodel.save()
    table_template = DatauploadTabletemplates.objects.get(
        table=table)
    try:
        column_bindings = json.loads(
            table_template.source_column_names)
    except:
        print("Json convert error")
    # -- Translation -- ##
    translate_unas(file=file, column_bindigs=column_bindings)
    # translate_categories()
    # -- Upload --##
    try:
        handle_uploaded_file(filename, table,
                             table_template, 1, False, column_bindings, True)
    except ValueError:
        uploadmodel.table = table
        uploadmodel.status = "error"
        uploadmodel.status_description = "Hibás fájl tartalom"
        uploadmodel.save()
        print("Could not upload file")
        return


def unas_translator_correcter():
    unas_correcter_ro()
    unas_correcter_sk()


def unas_image_upload():
    log("Unas képek feltöltése", "INFO", "unas_image_upload")
    file = get_unas_img_feed_url()
    table_template = DatauploadTabletemplates.objects.get(
        table="fol_unas_img")
    try:
        column_bindings = json.loads(
            table_template.source_column_names)
    except:
        print("Json convert error")
    uploadmodel = DatauploadUploadmodel(
        table="fol_unas_img", file=file, user_id=1, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
    uploadmodel.save()
    handle_uploaded_file(file=file, table="fol_unas_img",
                         table_template=table_template, user_id=1, is_new_table=False, column_bindings=column_bindings, is_feed=True)


def pen_adatlap_upload():
    log("Penészmentesítés adatlapok feltöltése",
        "INFO", script_name="pen_adatlap_upload")
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = '/home/atti/googleds/auth/pen/jutalék/dogwood-day-333815-db1f1cf5a4e8.json'
    SPREADSHEET_ID = '1kFMaObjL4Y3pQyrU6fi3D59-HOkr000XaOHnFS_6l90'
    RANGE_NAME = 'Datas!A:Z'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    values = result.get('values', [])

    file = "/home/atti/googleds/files/pen_adatlapok/pen_adatlapok.xlsx"
    df = pd.DataFrame(values[1:], columns=values[0])
    df.to_excel(file,
                index=False)
    table_template = DatauploadTabletemplates.objects.get(
        table="pen_adatlapok")
    try:
        column_bindings = json.loads(
            table_template.source_column_names)
    except:
        print("Json convert error")
    uploadmodel = DatauploadUploadmodel(
        table="pen_adatlapok", file=file, user_id=1, is_new_table=False, status_description="Feltöltésre kész", status="ready", upload_timestamp=datetime.now(), mode="Feed")
    uploadmodel.save()
    handle_uploaded_file(file=file, table="pen_adatlapok",
                         table_template=table_template, user_id=1, is_new_table=False, column_bindings=column_bindings, is_feed=True)


def fol_orders_delete_last_90():
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PORT = os.environ.get("DB_PORT")

    engine = create_engine('postgresql://'+DB_USER+':' +
                           DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

    engine.execute(
        f"DELETE FROM fol_orders WHERE \"Order_Date\" >= '{(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')}'")

    engine.execute(
        f"DELETE FROM pro_orders WHERE \"Order_Date\" >= '{(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')}'")


def sm_inventory_planner():
    sm_fetch_data()


def sm_auto_order():
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_PORT = os.environ.get("DB_PORT")

    engine = create_engine('postgresql://'+DB_USER+':' +
                           DB_PASS + '@'+DB_HOST+':'+DB_PORT+'/'+DB_NAME)

    df = pd.read_sql(
        "select vendor, need_permission from sm_vendor_data where budget <= to_order_cost;", con=engine)
    for i in df.loc:
        status = ""
        if i.need_permission == True:
            status = "DRAFT"
        else:
            status = "OPEN"
        inventory_planner(i.vendor, status=status, is_new=True)
