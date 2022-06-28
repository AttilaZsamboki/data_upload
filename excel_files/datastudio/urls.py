from django.urls import path
from . import views

urlpatterns = [
    path('data_upload/', views.FileFieldFormView.as_view(), name="upload"),
    path('home/', views.Home, name="home")
]
