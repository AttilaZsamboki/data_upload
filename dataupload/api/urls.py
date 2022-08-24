from xml.etree.ElementInclude import include
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    #---------------------------------DATAUPLOAD CONFIG---------------------------------------#
    path('templates/', views.TemplatesList.as_view()),
    path('templates/<int:pk>/', views.TemplateDetail.as_view()),
    path('special-queries/', views.SpecialQueriesList.as_view()),
    path('special-queries/<int:pk>/', views.SpecialQueryDetail.as_view()),
    #----------------------------------GENERIC------------------------------------#
    path('table-names', views.TableNames),
    path('column-names/', views.ColumnNames),
    #----------------------------------DATAS--------------------------------------#
    #-----------------------------------FOL---------------------------------------#
    path('fol_bevételek/', views.FolBevetelekList.as_view()),
    path('fol_bevételek/<int:pk>/', views.FolBevetelDetail.as_view()),
    path('fol_gls_elszámolás', views.FolGlsElszámolásList.as_view()),
    path('fol_gls_elszámolás/<int:pk>/', views.FolGlsElszámolásDetail.as_view()),
    path('fol_költségek/', views.FolKoltsegekList.as_view()),
    path('fol_költségek/<int:pk>/', views.FolKoltsegDetail.as_view()),
    path('fol_orders/', views.FolOrdersList.as_view()),
    path('fol_orders/<int:pk>/', views.FolOrderDetail.as_view()),
    path('fol_product_suppliers/', views.FolProductSuppliersList.as_view()),
    path('fol_product_suppliers/<int:pk>/',
         views.FolProductSupplierDetail.as_view()),
    path('fol_stock_report/', views.FolStockReportList.as_view()),
    path('fol_stock_report/<int:pk>/', views.FolStockReportDetail.as_view()),
    path('fol_számlák/', views.FolSzamlakList.as_view()),
    path('fol_számlák/<int:pk>', views.FolSzamlaDetail.as_view()),
    path('fol_unas/', views.FolUnasList.as_view()),
    path('fol_unas/<int:pk>', views.FolUnasDetail.as_view()),
    #-------------------------------PRO-------------------------------------------#
    path('pro_bevételek/', views.ProBevetelekList.as_view()),
    path('pro_bevételek/<int:pk>/', views.ProBevetelDetail.as_view()),
    path('pro_költségek/', views.ProKoltsegekList.as_view()),
    path('pro_költségek/<int:pk>/', views.ProKoltsegDetail.as_view()),
    path('pro_orders/', views.ProOrdersList.as_view()),
    path('pro_orders/<int:pk>/', views.ProOrderDetail.as_view()),
    path('pro_product_suppliers/', views.ProProductSuppliersList.as_view()),
    path('pro_product_suppliers/<int:pk>/',
         views.ProProductSupplierDetail.as_view()),
    path('pro_stock_report/', views.ProStockReportList.as_view()),
    path('pro_stock_report/<int:pk>/', views.ProStockReportDetail.as_view()),
    path('pro_számlák/', views.ProSzamlakList.as_view()),
    path('pro_számlák/<int:pk>', views.ProSzamlaDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
