from django.urls import path, include
from . import views

urlpatterns = [
    path('data_upload/', views.UploadFileView.as_view(), name="upload"),
    path('login/', views.login_view, name="login"),
    path('', views.Home, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('create-db-connection/', views.DatabaseConnectionCreate.as_view(), name="dbconnect"),
    path('list-db-connection/', views.DatabaseConnectionList.as_view(), name="dblist"),
    path('update-db-connection/<pk>', views.DatabaseConnectionUpdate.as_view(), name="dbupdate"),
    path('delete-db-connection/<pk>', views.DatabaseConnectionDelete.as_view(), name="dbdelete")
]
