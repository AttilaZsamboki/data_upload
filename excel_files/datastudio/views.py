import psycopg2
from requests import request
from .upload_handler import handle_uploaded_file
from .forms import UploadFileForm, DatabaseConnectionForm, ImportTemplateForm, TableTemplateForm
from .models import DatabaseConnections, ImportTemplates, TableTemplates
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from psycopg2 import connect

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
        connection_details = DatabaseConnections.objects.get(name=str(name), created_by=request.user.id)
        special_queries = ImportTemplates.objects.filter(table=table, created_by=request.user.id)
        table_template = TableTemplates.objects.get(table=table, created_by=request.user.id)
        if form.is_valid():
            for file in files:
                handle_uploaded_file(file, table, connection_details, special_queries, table_template)
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
        return super().form_valid(form) 

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

#Delete (cruD)
class DeleteTableTemplate(LoginRequiredMixin, DeleteView):
    model = TableTemplates
    template_name = "table_template_delete.html"
    success_url = reverse_lazy('table_templates')




# @login_required
# def DataVisualize(request):
#     if request.method == 'POST':
#         connection = request.POST['connection']
#         table = request.POST['table']
#         which = request.POST['which']
#         where = request.POST['where']
#         order = request.POST['order']
#         connection_details = DatabaseConnections.objects.get(name=str(connection))

#         DB_HOST = connection_details.host
#         DB_NAME = connection_details.database
#         DB_USER = connection_details.username
#         DB_PASS = connection_details.password
#         DB_PORT = connection_details.port
        
#         keepalive_kwargs = {
#             "keepalives": 1,
#             "keepalives_idle": 60,
#             "keepalives_interval": 10,
#             "keepalives_count": 5
#         }


#         conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
#                             password=DB_PASS, host=DB_HOST, port=DB_PORT, **keepalive_kwargs)

#         cur = conn.cursor()

#         cur.execute("SELECT \""+ which +"\" FROM \""+ table +"\" WHERE "+ where +" ORDER BY "+ order +";")

#     return render(request, "datavisualize.html")