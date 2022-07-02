from django.shortcuts import redirect, render
from requests import request
from .upload_handler import handle_uploaded_file
from .forms import UploadFileForm, SignUpForm
from .models import Users
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.contrib.auth import login, logout, authenticate


class FileFieldFormView(FormView):
    form_class = UploadFileForm
    template_name = 'upload.html'
    success_url = '/data_upload'

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        table = request.POST.get('table_name')
        if form.is_valid():
            for file in files:
                handle_uploaded_file(file, table)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email_address = request.POST["email_address"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("invalid credentials")
    return render(request, "login.html")

# class SignUpForm(FormView):
#     form_class = SignUpForm
#     template_name = 'sign_up.html'
#     success_url = '/datastudio/home'
#     def post(self, request):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

def Home(request):
    return render(request, "home.html")

class UsersView(ListView):
    model = Users

def logout_view(request):
    logout(request)
    return redirect("home")