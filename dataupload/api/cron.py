import os
from .models import UploadModel, ImportTemplates, TableTemplates
from .upload_handler import handle_uploaded_file


def upload_file():
    for upload in UploadModel.objects.all():
        table = upload.table
        file = upload.file
        model_extension_format = UploadModel.objects.filter(
            table=table, user_id=upload.user_id)[0].extension_format
        if model_extension_format == '':
            extension_format = TableTemplates.objects.get(
                table=table, created_by_id=upload.user_id).extension_format
        else:
            extension_format = model_extension_format
        special_queries = ImportTemplates.objects.filter(
            table=table, created_by=upload.user_id)
        table_template = TableTemplates.objects.get(
            table=table, created_by=upload.user_id)
        handle_uploaded_file(file, table, special_queries,
                             table_template, extension_format)

    UploadModel.objects.all().delete()
