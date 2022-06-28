from secrets import choice
from django import forms
from requests import request
from django.forms import ModelForm

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
    table_name = forms.CharField(label='Tábla neve?', widget=forms.Select(choices=TABLE_CHOICES))