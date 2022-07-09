from django.urls import path, include
from . import views

urlpatterns = [
    path('data_upload/', views.UploadFileView.as_view(), name="upload"),
    path('login/', views.login_view, name="login"),
    path('', views.Home, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('create-db-connection/', views.DatabaseConnectionCreate.as_view(), name="dbconnect"),
    path('db-connections/', views.DatabaseConnectionList.as_view(), name="dblist"),
    path('update-db-connection/<pk>', views.DatabaseConnectionUpdate.as_view(), name="dbupdate"),
    path('delete-db-connection/<pk>', views.DatabaseConnectionDelete.as_view(), name="dbdelete"),
    path('create-import-template/', views.CreateImportTemplate.as_view(), name="create_imp_template"),
    path('import-templates/', views.ReadImportTemplate.as_view(), name="import_templates"),
    path('update-import-template/<pk>', views.UpdateImportTemplate.as_view(), name="update_imp_template"),
    path('delete-import-template/<pk>', views.DeleteImportTemplate.as_view(), name="delete_imp_template"),
]
