from django.urls import path
from . import views

urlpatterns = [
    path('data_upload/', views.FileFieldFormView.as_view(), name="upload"),
    path('login/', views.login_view, name='login'),
    # path('signup/', views.SignUpForm.as_view(), name='signup'),
    path('', views.Home, name="home"),
    path('users/list', views.UsersView.as_view(), name='usersList'),
    path('logout/', views.logout_view, name="logout")
]
