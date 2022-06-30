from cProfile import label
import email
from secrets import choice
from django import forms
from idna import alabel
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

class LoginForm(forms.Form):
    email_address = forms.EmailField(label='Email address')
    password = forms.PasswordInput()

class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email_address = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_again = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')