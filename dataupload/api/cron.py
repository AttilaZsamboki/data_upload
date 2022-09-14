from base64 import urlsafe_b64decode
from django.db import connection
import os
import json
from .models import DatauploadUploadmodel, DatauploadImporttemplates, DatauploadTabletemplates
from .upload_handler import handle_uploaded_file
import requests
from datetime import date, datetime
from .utils.utils import diff_month
from .utils.gmail import send_message, gmail_authenticate
import requests


def upload_file():
    for upload in DatauploadUploadmodel.objects.all():
        table, file, is_new_table, skiprows, status = (
            upload.table, upload.file, upload.is_new_table, upload.skiprows, upload.status)
        if status == "ready" or status == "under upload":
            if not is_new_table:
                special_queries = DatauploadImporttemplates.objects.filter(
                    table=table, created_by_id=upload.user_id)
                table_template = DatauploadTabletemplates.objects.get(
                    table=table)
                skiprows = table_template.skiprows
                try:
                    column_bindings = json.loads(
                        table_template.source_column_names)
                except:
                    print("Json convert error")
            else:
                special_queries = {}
                table_template = {}
                column_bindings = {}
            handle_uploaded_file(file, table, special_queries,
                                 table_template, upload.user_id, is_new_table, skiprows, column_bindings, False)


def upload_feed():
    UPLOADS = [
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGWjVGQW0tTi1JcmJYNjg4Yl83UnB6QjhTT0U4d1hTczhjQUQyZllxSWV4MFcwZ1lmaEQtQmhZcWVxUVBzNWhRWjVqZTh3NzNSdlo4NGFOOGdyTloyTmxLV3lTelp1MEtuOVBYVkxGdHBkNjVSbVE9", "table": "fol_stock_report", "owner": 1},
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGYXhMWDA5c3NZZ3NfaW5ic21QTkJfQ2JmM2V4NXJ0aXM5THIxUmJmbHpxaTdtb0c3bkt1MGZUcmtsZm5vLV9aVEx4OFNOUVM3d3lrVkx0YzZfTFBWMENfR0JHVjhNc3BWWlNxSURSaDhxTnNQd1E9",
            "table": "fol_stock_transaction_report", "owner": 1},
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGaHZXZkdYREUxQ1diSXVlT1ptaTNaV1RNbnFkZ0ZsTEhLTkpjMHdLSWQ3MFVuT2N6ZWJjUUg0ejh6azA4LThxNlh5VTB2ZGlreXVIZjlQSmZYbGdseTdwNkxFX05BU3JPdDRJOXlweldwdkt2UVk9", "table": "pro_orders", "owner": 3},
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGaHZXeDRoMU1FRzMzWmNkRGVMWnFHNHdrM0c0MVpsRkhEaEV6OE15NENRdlNpOFE1TXJhS3VUNTkwbUljOWF5N0w5NENDdkNtc3d4c0xtT09aWnJBcHVMdHQ0emF0d0NQTmpQTmJEalR0SzM1c0U9", "table": "pro_products"},
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpHdUd3aFJkbWc5dnkwNWloQjYtYlVnaTBISzdrTU9qc05oQU5sMnlzRGQwYmVuam9WNWZhcVlWandUNEQ2NDZLR1hONlhVNkh1d3BjM3pHbEpvc1pPT2hLeFl3dms5aVdxVXVVX1NtUWdLaGg0ZGc9", "table": "fol_product_suppliers"},
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGeEt1ZnUtdHljSU0yanozZnp0bHlHeC04R2NoZ0F3eG1IakxBYldVZnZhOG43OXhORDc5OGVNN2lJMkkxLUtVTTBHSG90czhfZEs4UHVONHE3bEZLdnZLd183SHRWWU5icUNmSmY4Zl9IdnpLdlU9", "table": "pro_product_suppliers"},
        {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGaHZXWFlFYzQ2bkctRUdtXzdzaTRPV213WW50RTA3UV9zOVYtOE5Va3dTYkotWFM2OW9rWkQ2cDk1LXlVSkN5Q3VOcmdzalhodTIxdkszUHhCR0xpdS1CZW9xb3hkYmFULXpKVDB3YnN6MGZ2UDQ9", "table": "pro_stock_report", "owner": 3}]
    for upload in UPLOADS:
        try:
            file = requests.get(upload["url"]).content
        except:
            print("Not valid url for file")
            continue
        if upload["table"] == "pro_stock_report":
            open(
                f"/home/atti/googleds/files/profishop/stock_report/{date.today()}.xlsx", "wb").write(file)
        elif upload["table"] == "fol_stock_report":
            open(
                f"/home/atti/googleds/files/foliasjuci/stock_report/{date.today()}.xlsx", "wb").write(file)
        special_queries = DatauploadImporttemplates.objects.filter(
            table=upload["table"])
        table_template = DatauploadTabletemplates.objects.get(
            table=upload["table"])
        skiprows = table_template.skiprows
        try:
            column_bindings = json.loads(
                table_template.source_column_names)
        except:
            print("Json convert error")
        try:
            handle_uploaded_file(file, upload["table"], special_queries,
                                 table_template, upload["owner"], False, skiprows, column_bindings, True)
        except:
            print("Could not upload file")
            continue


def delete_log():
    for upload in DatauploadUploadmodel.objects.all():
        if diff_month(upload.upload_timestamp, datetime.now()) < -1:
            upload.delete()


def order_feed():
    UPLOADS = [{"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGWjVGWlN4Yk5TY25WUl9iRU1XMjNWY2dUUTJQdzU0WUZObWhDb0RhcmRJVnZBZm1VU1JXQ1NTeDRCZ3ZuMmx4NmxwYzZqczhOTFBySTZWbTBONUNTQXBvaFhjRXZQQzRqN0dkaWVjSGFJMTIxNE09", "table": "fol_orders"}]
    for upload in UPLOADS:
        try:
            file = requests.get(upload["url"]).content
        except:
            print("Not valid url for file")
            continue
        if upload["table"] == "pro_stock_report":
            open(
                f"/home/atti/googleds/files/profishop/stock_report/{date.today()}.xlsx", "wb").write(file)
        elif upload["table"] == "fol_stock_report":
            open(
                f"/home/atti/googleds/files/foliasjuci/stock_report/{date.today()}.xlsx", "wb").write(file)
        special_queries = DatauploadImporttemplates.objects.filter(
            table=upload["table"])
        table_template = DatauploadTabletemplates.objects.get(
            table=upload["table"])
        skiprows = table_template.skiprows
        try:
            column_bindings = json.loads(
                table_template.source_column_names)
        except:
            print("Json convert error")
        try:
            handle_uploaded_file(file, upload["table"], special_queries,
                                 table_template, 1, False, skiprows, column_bindings, True)
        except:
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
                                filepath = os.path.join(folder_name, filename)
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
                                        "results"] if i["email"] == sender_email]
                                    user_id = user[0]["userId"]
                                    tables = [i for i in connection.introspection.table_names(
                                    ) if i[0:3] == user[0]["name"][0:3]]
                                    table = ""
                                    for i in tables:
                                        if i.lower()[4:] in filename.lower().replace("-", "-"):
                                            table = i
                                    if table == "":
                                        send_message(service, sender_email, "Feltöltés hiba",
                                                     f"'{filename}' nem megfelelő fájlnév, tartalmaznia kell egy tábla nevét az aláábiak közül: {', '.join([i[4:] for i in tables])}", [])
                                    special_queries = DatauploadImporttemplates.objects.filter(
                                        table=table)
                                    table_template = DatauploadTabletemplates.objects.get(
                                        table=table)
                                    skiprows = table_template.skiprows
                                    column_bindings = json.loads(
                                        table_template.source_column_names)
                                    with open(filepath, "wb") as f:
                                        f.write(urlsafe_b64decode(data))
                                    handle_uploaded_file(file=filepath, table=table, special_queries=special_queries,
                                                         table_template=table_template, user_id=user_id, is_new_table=False, skiprows=skiprows, column_bindings=column_bindings, is_feed=False, is_email=True, sender_email=sender_email)

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
                    "/home/atti/googleds/dataupload/media/upload_files", message, sender_email)
        print("="*50)

    def delete_messages(service, query):
        messages_to_delete = search_messages(service, query)
        for msg in messages_to_delete:
            # it's possible to delete a single message with the delete API, like this:
            service.users().messages().delete(
                userId='me', id=msg["id"]).execute()
        # but it's also possible to delete all the selected messages with one query, batchDelete

    service = gmail_authenticate()

    results = search_messages(service, "Feltöltés")
    print(f"Found {len(results)} results.")

    for msg in results:
        read_message(service, msg)
    delete_messages(service, "Feltöltés")
