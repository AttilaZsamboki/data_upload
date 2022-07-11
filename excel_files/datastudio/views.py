import psycopg2
from requests import request
from .upload_handler import handle_uploaded_file
from .forms import UploadFileForm, DatabaseConnectionForm, ImportTemplateForm, TableTemplateForm, UploadFileForm
from .models import DatabaseConnections, ImportTemplates, TableTemplates, UploadModel
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from psycopg2 import connect

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = UploadModel(table=request.POST["table"], file=request.FILES['file'], user_id=request.user.id, extension_format=request.POST['extension_format'])
            instance.save()
            return HttpResponseRedirect('/upload')
    else:
        form = UploadFileForm()
    
    table_choices = TableTemplates.objects.filter(created_by=request.user.id)
    context = {'form': form, 'table_choices': table_choices}

    return render(request, 'upload.html', context)

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

@login_required
def Home(request):
    return render(request, "home.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# -------------------------------------------------------------------- DATABASE CONNECTIONS --------------------------------------------------------------------------#

#CRUD database connections
#Read (cRud)
class DatabaseConnectionList(LoginRequiredMixin, ListView):
    model = DatabaseConnections
    template_name = "connections.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["connection_details"] = DatabaseConnections.objects.filter(created_by=self.request.user.id)
        return context

#Create (Crud)
class DatabaseConnectionCreate(LoginRequiredMixin, CreateView):
    model = DatabaseConnections
    template_name = "connection_create.html"
    form_class = DatabaseConnectionForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form) 

#Update (crUd)
class DatabaseConnectionUpdate(LoginRequiredMixin, UpdateView):
    model = DatabaseConnections
    template_name = "connection_update.html"
    fields = ("name",
                  "host",
                  "database",
                  "username",
                  "password")
    success_url = reverse_lazy('dblist')

#Delete (cruD)
class DatabaseConnectionDelete(LoginRequiredMixin, DeleteView):
    model = DatabaseConnections
    template_name = "connection_delete.html"
    success_url = reverse_lazy('dblist')


# -------------------------------------------------------------------- IMPORT TEMPLATES -----------------------------------------------------------------------------#

#CRUD import templates
#Create (Crud)
class CreateImportTemplate(LoginRequiredMixin, CreateView):
    model = ImportTemplates
    template_name = "import_template_create.html"
    form_class = ImportTemplateForm
    success_url = reverse_lazy('import_templates')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form) 

#Read (cRud)
class ReadImportTemplate(LoginRequiredMixin, ListView):
    model = ImportTemplates
    template_name = "import_templates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["import_templates"] = ImportTemplates.objects.filter(created_by=self.request.user.id)
        return context

#Update (crUd)
class UpdateImportTemplate(LoginRequiredMixin, UpdateView):
    model = ImportTemplates
    template_name = "import_template_update.html"
    form_class = ImportTemplateForm
    success_url = reverse_lazy('import_templates')

#Delete (cruD)
class DeleteImportTemplate(LoginRequiredMixin, DeleteView):
    model = ImportTemplates
    template_name = "import_template_delete.html"
    success_url = reverse_lazy('import_templates')


# -------------------------------------------------------------------- TABLE TEMPLATES -----------------------------------------------------------------------------#

#CRUD import templates
#Create (Crud)

class CreateTableTemplate(LoginRequiredMixin, CreateView):
    model = TableTemplates
    template_name = "table_template_create.html"
    form_class = TableTemplateForm
    success_url = reverse_lazy('table_templates')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.database = self.request.POST["database"]
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["db_choices"] = DatabaseConnections.objects.filter(created_by=self.request.user.id)
        return context

#Read (cRud)
class ReadTableTemplate(LoginRequiredMixin, ListView):
    model = TableTemplates
    template_name = "table_templates.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_templates"] = TableTemplates.objects.filter(created_by=self.request.user.id)
        return context

#Update (crUd)
class UpdateTableTemplate(LoginRequiredMixin, UpdateView):
    model = TableTemplates
    template_name = "table_template_update.html"
    form_class = TableTemplateForm
    success_url = reverse_lazy('table_templates')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["db_choices"] = DatabaseConnections.objects.filter(created_by=self.request.user.id)
        return context

#Delete (cruD)
class DeleteTableTemplate(LoginRequiredMixin, DeleteView):
    model = TableTemplates
    template_name = "table_template_delete.html"
    success_url = reverse_lazy('table_templates')