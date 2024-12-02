import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
import pandas as pd
from .models import DatauploadUploadmodel, DatauploadTabletemplates
from channels.db import database_sync_to_async
from .utils.upload import col_by_dtype

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")


class UploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.upload_id = self.scope["url_route"]["kwargs"]["upload_id"]
        self.upload_group_name = 'upload_%s' % self.upload_id
        self.upload = await self.get_upload()
        self.template = await self.get_template()
        file = self.upload.file
        await self.channel_layer.group_add(
            self.upload_group_name,
            self.channel_name
        )
        filename, extension_format = os.path.splitext(str(self.upload.file))
        accepted_formats = [".xlsx", ".csv", ".xls", ".tsv"]
        if extension_format in accepted_formats:
            self.form_over_stat = True
        else:
            self.form_over_stat = False
        if not self.form_over_stat:
            await self.channel_layer.group_send(
                self.upload_group_name,
                {
                    "type": "status",
                    "extension_format": {
                        "overall_status": self.form_over_stat,
                        "gotten": extension_format,
                        "expected": ", ".join(accepted_formats),
                    },
                    "column_names": {
                        "overall_status": "",
                        "missing_cols": "",
                        "wrong_cols": "",
                        "gotten": "",
                        "expected": "",
                    },
                    "column_content": {
                        "overall_status": "",
                        "error": ""
                    }
                }
            )
        else:
            if extension_format == '.csv':
                data = pd.read_csv(file, skiprows=int(self.template.skiprows))
            elif extension_format == '.tsv':
                data = pd.read_csv(file, skiprows=int(
                    self.template.skiprows), delimiter='\t')
            else:
                data = pd.read_excel(
                    file, skiprows=int(self.template.skiprows))
            df = pd.DataFrame(data)
            self.source_column_names_raw = {k: v for k, v in sorted(json.loads(
                self.template.source_column_names).items(), key=lambda item: item[1])}
            self.source_column_names = ", ".join(
                list(self.source_column_names_raw.values()))
            self.gotten_column_names = ", ".join(df.columns.sort_values())
            self.wrong_cols = ", ".join(
                list(set(self.gotten_column_names.split(", ")) - set(self.source_column_names.split(", "))))
            if self.template.table == "pro_költségek":
                missing_cols = list(set(self.source_column_names.split(
                    ", ")) - set(self.gotten_column_names.split(", ")))
                cols_to_remove = [
                    "1_alkategoria", "2_alkategoria", "3_alkategoria", "4_alkategoria"]
                missing_cols = [
                    i for i in missing_cols if i not in cols_to_remove]
            else:
                missing_cols = list(set(self.source_column_names.split(
                    ", ")) - set(self.gotten_column_names.split(", ")))
            self.missing_cols = ", ".join(missing_cols)
            if self.missing_cols:
                self.column_over_stat = False
            else:
                self.column_over_stat = True
            numeric_cols = col_by_dtype(['decimal', 'numeric', 'real', 'double precision',
                                        'smallserial', 'serial', 'bigserial', 'money', 'bigint'], self.upload.table)
            date_cols = col_by_dtype(['date', 'timestamp'], self.upload.table)
            numeric_cols_source = [
                j for i, j in self.source_column_names_raw.items() if i in numeric_cols] if numeric_cols else []
            date_cols_source = [
                j for i, j in self.source_column_names_raw.items() if i in date_cols] if date_cols else []
            column_content_stat = True
            column_content_error = []
            if self.template.table == 'fol_gls_elszámolás':
                df = df[df['Súly'].notna()]
            for i in df.columns:
                try:
                    if numeric_cols_source and i in numeric_cols_source:
                        lst = []
                        for x in df[i]:
                            if type(x) == str and ',' in x:
                                lst.append(x.replace(',', '.'))
                            else:
                                lst.append(x)
                        df[i] = lst
                        df[i] = df[i].astype(float)
                    if date_cols_source and i in date_cols_source:
                        df[i] = df[i].astype(dtype='datetime64[ns]')
                except ValueError as e:
                    column_content_stat = False
                    column_content_error.append(
                        {"error_col": str(i), "error": str(e)})
            await self.channel_layer.group_send(
                self.upload_group_name,
                {
                    "type": "status",
                    "extension_format": {
                        "overall_status": self.form_over_stat,
                        "gotten": extension_format,
                        "expected": ", ".join(accepted_formats),
                    },
                    "column_names": {
                        "overall_status": self.column_over_stat,
                        "missing_cols": self.missing_cols,
                        "wrong_cols": self.wrong_cols,
                        "gotten": self.gotten_column_names,
                        "expected": self.source_column_names,
                    },
                    "column_content": {
                        "overall_status": column_content_stat,
                        "error": column_content_error
                    }
                }
            )

    @database_sync_to_async
    def get_template(self):
        return DatauploadTabletemplates.objects.get(table=self.upload.table)

    @database_sync_to_async
    def get_upload(self):
        return DatauploadUploadmodel.objects.get(id=self.upload_id)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.upload_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if json.loads(text_data)["upload"]:
            await self.set_upload_status()

    @database_sync_to_async
    def set_upload_status(self):
        upload = DatauploadUploadmodel.objects.get(id=self.upload_id)
        setattr(upload, "status", "ready")
        setattr(upload, "status_description", "Feltöltésre vár")
        upload.save()

    async def status(self, event):
        await self.send(text_data=json.dumps({
            "extension_format": {
                        "overall_status": event["extension_format"]["overall_status"],
                        "gotten": event["extension_format"]["gotten"],
                        "expected": event["extension_format"]["expected"],
                        },
            "column_names": {
                "overall_status": event["column_names"]["overall_status"],
                "missing_cols": event["column_names"]["missing_cols"],
                "wrong_cols": event["column_names"]["wrong_cols"],
                "gotten": event["column_names"]["gotten"],
                "expected": event["column_names"]["expected"],
            },
            "column_content": {
                "overall_status": event["column_content"]["overall_status"],
                "error": event["column_content"]["error"]
            }
        }))


class UploadDeleteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.upload_id = self.scope["url_route"]["kwargs"]["upload_id"]
        self.upload = await self.get_upload()
        self.upload_group_name = 'upload_%s' % self.upload_id
        await self.delete_upload()
        if self.upload.status != "success":
            os.remove(
                f'/app/media/{self.upload.file}')
        else:
            os.remove(str(self.upload.file))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.upload_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def delete_upload(self):
        upload = DatauploadUploadmodel.objects.get(id=self.upload_id)
        upload.delete()

    @database_sync_to_async
    def get_upload(self):
        return DatauploadUploadmodel.objects.get(id=self.upload_id)


class SMOrderConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            "sm_order",
            self.channel_name
        )

    async def receive(self, text_data=None):
        await self.channel_layer.group_send(
            "sm_order",
            {
                "type": "order_status_change",
                "message": text_data["message"],
                "progress_value": text_data["progress_value"]
            }
        )

    async def order_status_change(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "progress_value": event["progress_value"]
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            "sm_order",
            self.channel_name
        )
