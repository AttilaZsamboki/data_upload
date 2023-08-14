from datetime import datetime, timedelta
import django
import os
import sys

sys.path.append(os.path.abspath('/home/atti/googleds/dataupload'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "dataupload.dataupload.settings")
django.setup()