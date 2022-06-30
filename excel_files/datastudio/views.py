from django.shortcuts import render
from requests import request
from .upload_handler import handle_uploaded_file
from .forms import UploadFileForm, LoginForm, SignUpForm
from .models import Users
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import ListView


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

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/datastudio/home'

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
