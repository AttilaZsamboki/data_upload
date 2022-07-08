from requests import request
from .upload_handler import handle_uploaded_file
from .forms import UploadFileForm, DatabaseConnectionForm
from .models import DatabaseConnections
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class UploadFileView(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'upload.html'
    success_url = '/data_upload'

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        table = request.POST.get('table_name')
        name = request.POST.get('name') 
        connection_details = DatabaseConnections.objects.get(name=str(name))
        if form.is_valid():
            for file in files:
                handle_uploaded_file(file, table, connection_details)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["db_choices"] = DatabaseConnections.objects.filter(created_by=self.request.user.id)
        return context

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return HttpResponse("Invalid credentials")
    return render(request, "login.html")

def Home(request):
    return render(request, "home.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


class DatabaseConnectionList(LoginRequiredMixin, ListView):
    model = DatabaseConnections
    template_name = "connections.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["connection_details"] = DatabaseConnections.objects.filter(created_by=self.request.user.id)
        return context

class DatabaseConnectionCreate(LoginRequiredMixin, CreateView):
    model = DatabaseConnections
    template_name = "connection_create.html"
    form_class = DatabaseConnectionForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form) 

class DatabaseConnectionUpdate(LoginRequiredMixin, UpdateView):
    model = DatabaseConnections
    template_name = "connection_update.html"
    fields = ("name",
                  "host",
                  "database",
                  "username",
                  "password")
    success_url = reverse_lazy('dblist')

class DatabaseConnectionDelete(LoginRequiredMixin, DeleteView):
    model = DatabaseConnections
    template_name = "connection_delete.html"
    success_url = reverse_lazy('dblist')