import json
from .models import DatauploadUploadmodel, DatauploadImporttemplates, DatauploadTabletemplates
from .upload_handler import handle_uploaded_file
import os
import requests
from datetime import date, datetime
from .utils.utils import diff_month


def upload_file():
    for upload in DatauploadUploadmodel.objects.all():
        table, file, is_new_table, skiprows, status = (
            upload.table, upload.file, upload.is_new_table, upload.skiprows, upload.status)
        if status == "ready":
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
    UPLOADS = [{"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGWjVGWlN4Yk5TY25WUl9iRU1XMjNWY2dUUTJQdzU0WUZObWhDb0RhcmRJVnZBZm1VU1JXQ1NTeDRCZ3ZuMmx4NmxwYzZqczhOTFBySTZWbTBONUNTQXBvaFhjRXZQQzRqN0dkaWVjSGFJMTIxNE09", "table": "fol_orders"},
               {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGWjVGQW0tTi1JcmJYNjg4Yl83UnB6QjhTT0U4d1hTczhjQUQyZllxSWV4MFcwZ1lmaEQtQmhZcWVxUVBzNWhRWjVqZTh3NzNSdlo4NGFOOGdyTloyTmxLV3lTelp1MEtuOVBYVkxGdHBkNjVSbVE9", "table": "fol_stock_report"},
               {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGYXhMWDA5c3NZZ3NfaW5ic21QTkJfQ2JmM2V4NXJ0aXM5THIxUmJmbHpxaTdtb0c3bkt1MGZUcmtsZm5vLV9aVEx4OFNOUVM3d3lrVkx0YzZfTFBWMENfR0JHVjhNc3BWWlNxSURSaDhxTnNQd1E9", "table": "fol_stock_transaction_report"},
               {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGaHZXZkdYREUxQ1diSXVlT1ptaTNaV1RNbnFkZ0ZsTEhLTkpjMHdLSWQ3MFVuT2N6ZWJjUUg0ejh6azA4LThxNlh5VTB2ZGlreXVIZjlQSmZYbGdseTdwNkxFX05BU3JPdDRJOXlweldwdkt2UVk9", "table": "pro_orders"},
               {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGaHZXWFlFYzQ2bkctRUdtXzdzaTRPV213WW50RTA3UV9zOVYtOE5Va3dTYkotWFM2OW9rWkQ2cDk1LXlVSkN5Q3VOcmdzalhodTIxdkszUHhCR0xpdS1CZW9xb3hkYmFULXpKVDB3YnN6MGZ2UDQ9", "table": "pro_stock_report"},
               {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGaHZXeDRoMU1FRzMzWmNkRGVMWnFHNHdrM0c0MVpsRkhEaEV6OE15NENRdlNpOFE1TXJhS3VUNTkwbUljOWF5N0w5NENDdkNtc3d4c0xtT09aWnJBcHVMdHQ0emF0d0NQTmpQTmJEalR0SzM1c0U9", "table": "pro_products"},
               {"url": "https://app.clouderp.hu/api/1/automatism/file-share/?s=Z0FBQUFBQmpGeEt1ZnUtdHljSU0yanozZnp0bHlHeC04R2NoZ0F3eG1IakxBYldVZnZhOG43OXhORDc5OGVNN2lJMkkxLUtVTTBHSG90czhfZEs4UHVONHE3bEZLdnZLd183SHRWWU5icUNmSmY4Zl9IdnpLdlU9", "table": "pro_product_suppliers"}]
    for upload in UPLOADS:
        try:
            file = requests.get(upload["url"]).content
        except:
            print("Not valid url for file")
        open(
            f"/home/atti/googleds/files/profishop/stock_report/{date.today()}", "wb").write(file)
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
        handle_uploaded_file(file, upload["table"], special_queries,
                             table_template, 1, False, skiprows, column_bindings, True)


def delete_log():
    for upload in DatauploadUploadmodel.objects.all():
        if diff_month(upload.upload_timestamp, datetime.now()) < -1:
            upload.delete()
