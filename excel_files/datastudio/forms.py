from enum import unique
from django import forms
from .models import DatabaseConnections, ImportTemplates, TableTemplates

TABLE_CHOICES = [
    ('bevételek', 'Bevételek'),
    ('gls_elszámolás', 'GLS'),
    ('költségek', 'Költségek'),
    ('orders', 'Rendelések'),
    ('product_suppliers', 'Beszállítók'),
    ('stock_report', 'Készlet'),
    ('számlák', 'Számlák'),
    ('unas', 'Unas'),
]


class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    table_name = forms.CharField(label='Tábla', widget=forms.Select(choices=TABLE_CHOICES))

class DatabaseConnectionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = DatabaseConnections
        fields = ("name",
                  "host",
                  "database",
                  "username",
                  "password")

class ImportTemplateForm(forms.ModelForm):
    name = forms.CharField(label="Template name", required=False)
    table = forms.CharField(label="Table")
    special_query = forms.CharField(label="Query", help_text="IMPORTANT: Use temporary for the table name!", widget=forms.Textarea(attrs={"rows": 3}))
    class Meta:
        model = ImportTemplates
        fields = ("name", "table", "special_query")

# TABLE TEMPLATE
class TableTemplateForm(forms.ModelForm):
    pkey_col = forms.CharField(label="Primary key column")
    class Meta:
        model = TableTemplates
        fields = ("table", "pkey_col", "skiprows", "append")

# class DataVisualizationForm(forms.Form):
#     connection = forms.CharField
#     table
#     which
#     where
#     order
        