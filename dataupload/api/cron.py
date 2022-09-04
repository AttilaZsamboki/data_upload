import json
from .models import DatauploadUploadmodel, DatauploadImporttemplates, DatauploadTabletemplates
from .upload_handler import handle_uploaded_file
import os


def upload_file():
    for actual_file in os.listdir('/home/atti/googleds/dataupload/media/upload_files'):
        actual_file = f'upload_files/{actual_file}'
        assumed_files_raw = DatauploadUploadmodel.objects.values('file')
        if assumed_files_raw:
            for i in assumed_files_raw:
                assumed_files = [l for j, l in i.items()]
            if actual_file not in assumed_files:
                os.remove(
                    f'/home/atti/googleds/dataupload/media/{actual_file}')
        else:
            os.remove(f'/home/atti/googleds/dataupload/media/{actual_file}')
    for upload in DatauploadUploadmodel.objects.all():
        table, file, is_new_table, skiprows, status = (
            upload.table, upload.file, upload.is_new_table, upload.skiprows, status)
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
                                 table_template, upload.user_id, is_new_table, skiprows, column_bindings)
