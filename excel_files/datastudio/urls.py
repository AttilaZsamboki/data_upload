from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('upload/', views.upload_file, name="upload"),

# --------------------------------------------------------------- AUTHORIZATION --------------------------------------------------------------------------------------#

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

# --------------------------------------------------------------- DATABASE CONNECTIONS -------------------------------------------------------------------------------#

    path('create-db-connection/', views.DatabaseConnectionCreate.as_view(), name="dbconnect"),
    path('db-connections/', views.DatabaseConnectionList.as_view(), name="dblist"),
    path('update-db-connection/<pk>', views.DatabaseConnectionUpdate.as_view(), name="dbupdate"),
    path('delete-db-connection/<pk>', views.DatabaseConnectionDelete.as_view(), name="dbdelete"),

# ---------------------------------------------------------------- IMPORT TEMPLATES ----------------------------------------------------------------------------------#

    path('create-import-template/', views.CreateImportTemplate.as_view(), name="create_imp_template"),
    path('import-templates/', views.ReadImportTemplate.as_view(), name="import_templates"),
    path('update-import-template/<pk>', views.UpdateImportTemplate.as_view(), name="update_imp_template"),
    path('delete-import-template/<pk>', views.DeleteImportTemplate.as_view(), name="delete_imp_template"),

# ---------------------------------------------------------------- TABLE TEMPLATES -----------------------------------------------------------------------------------#

    path('create-table-template/', views.CreateTableTemplate.as_view(), name="create_tab_template"),
    path('table-templates/', views.ReadTableTemplate.as_view(), name="table_templates"),
    path('update-table-template/<pk>', views.UpdateTableTemplate.as_view(), name="update_tab_template"),
    path('delete-table-template/<pk>', views.DeleteTableTemplate.as_view(), name="delete_tab_template"),
]
