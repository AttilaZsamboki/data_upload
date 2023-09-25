from ..utils.base_path import base_path

from dotenv import load_dotenv

import django
import os
import sys
import json

load_dotenv()

sys.path.append(os.path.abspath(f"{base_path}/dataupload"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "dataupload.dataupload.settings")
django.setup()
from api.models import DatauploadTabletemplates, DatauploadUploadmodel  # noqa
from api.upload_handler import handle_uploaded_file  # noqa

table = "pen_products"
template = DatauploadTabletemplates.objects.get(
    table=table)
    
file = f"files/tests/{table}.xlsx"
model = DatauploadUploadmodel(table=table, file=file, user_id=1, is_new_table=False, status_description="Test", status="ready", mode="Feed")
model.save()

try:
    handle_uploaded_file(file=file, table=table, table_template=template, user_id=1, is_feed=False, is_new_table=False, column_bindings=json.loads(template.source_column_names))
except Exception as e:
    print(e)
    model.delete()