from django import forms
from .models import DatabaseConnections, ImportTemplates, TableTemplates, UploadModel

EXT_CHOICES = [
    ('', ''),
    ('xslx', 'xlsx'),
    ('csv', 'csv'),
    ('tsv', 'tsv'),
]

class UploadFileForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    extension_format = forms.ChoiceField(label="Extension format:", choices=EXT_CHOICES, required=False, help_text="IF NULL: given in table template")

    class Meta:
        model = UploadModel
        fields = ('file', 'extension_format',) 

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
    extension_format = forms.ChoiceField(label="Extension format:", choices=EXT_CHOICES)

    class Meta:
        model = TableTemplates
        fields = ("table", "pkey_col", "skiprows","extension_format", "append")
