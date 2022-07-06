from django.urls import path, include
from . import views

urlpatterns = [
    path('data_upload/', views.FileFieldFormView.as_view(), name="upload"),
    path('login/', views.login_view, name="login"),
    # path("account/", include("django.contrib.auth.urls"), name="login"),
    path('', views.Home, name="home"),
    path('users/list', views.UsersView.as_view(), name='usersList'),
    path('logout/', views.logout_view, name="logout")
]
