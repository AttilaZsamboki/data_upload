import os
from .models import DatauploadUploadmodel, DatauploadImporttemplates, DatauploadTabletemplates
from .upload_handler import handle_uploaded_file


def upload_file():
    for upload in DatauploadUploadmodel.objects.all():
        table, file, is_new_table = upload
        if not is_new_table:
            extension_format = DatauploadTabletemplates.objects.get(
                table=table, created_by_id=upload.user_id).extension_format
        special_queries = DatauploadImporttemplates.objects.filter(
            table=table, created_by_id=upload.user_id)
        table_template = DatauploadTabletemplates.objects.get(
            table=table, created_by_id=upload.user_id)
        handle_uploaded_file(file, table, special_queries,
                             table_template, extension_format, upload.user_id, is_new_table)
