from cProfile import label
import email
from secrets import choice
from django import forms
from idna import alabel
from requests import request
from django.forms import ModelForm
from .models import DatabaseConnections

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
        