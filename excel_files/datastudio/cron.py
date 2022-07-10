import os
from .models import UploadModel, DatabaseConnections, ImportTemplates, TableTemplates
from .upload_handler import handle_uploaded_file

def upload_file():
    for upload in UploadModel.objects.all():
        table = upload.table
        file = upload.file
        connection_details = DatabaseConnections.objects.get(name=upload.database)
        special_queries = ImportTemplates.objects.filter(table=table, created_by=upload.user_id)
        table_template = TableTemplates.objects.get(table=table, created_by=upload.user_id)
        handle_uploaded_file(file, table, connection_details, special_queries, table_template)

        os.remove('/home/atti/googleds/excel_files/media/' + str(file))
    UploadModel.objects.all().delete()