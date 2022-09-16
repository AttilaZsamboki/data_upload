from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('adatok/', views.main),
    path('upload/', views.main),
    path('profile/', views.main),
    path('logout/', views.main),
    path('login/', views.main),
    path('signup/', views.main),
    path('reset/', views.main),
    path('import-config/', views.main),
    path('add-templates/', views.main),
    path('add-special-queries/', views.main),
    path('create-table/', views.main),
    path('uploads/', views.main),
    path('upload-start/', views.main),
    path('upload-checker/', views.main),
    path('upload-tester/', views.main),
    path("add-table-overview/", views.main),
    path("add-feed/", views.main)
]
