from django.urls import path
from . import views

urlpatterns = [
    path('data_upload/', views.FileFieldFormView.as_view(), name="upload"),
    path('login/', views.LoginFormView.as_view(), name='login'),
    # path('signup/', views.SignUpForm.as_view(), name='signup'),
    path('home/', views.Home, name="home"),
    path('users/list', views.UsersView.as_view(), name='usersList')
]
