from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("download-log/", views.DownloadFile),
    path("upload-profile-image/", views.UploadProfileImg),
    #---------------------------------DATAUPLOAD CONFIG---------------------------------------#
    path("groups/", views.GroupsList.as_view()),
    path("groups/<str:pk>/", views.GroupsDetail.as_view()),
    path('templates/', views.TemplatesList.as_view()),
    path('templates/<int:pk>/', views.TemplateDetail.as_view()),
    path('uploadmodel/', views.UploadmodelList.as_view()),
    path('uploadmodel/<int:pk>/', views.UploadmodelDetail.as_view()),
    path('table-overview/', views.TableOverviewList.as_view()),
    path('table-overview/<int:pk>/', views.TableOverviewDetail.as_view()),
    path('feed/', views.FeedList.as_view()),
    path('feed/<str:pk>/', views.FeedDetail.as_view()),
    #----------------------------------GENERIC------------------------------------#
    path('table-names/', views.TableNames),
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

    path('fol_stock_transaction_report/',
         views.FolStockTransactionReportList.as_view()),
    path('fol_stock_transaction_report/<int:pk>/',
         views.FolStockTransactionReportDetail.as_view()),

    path('fol_stock_aging/',
         views.FolStockAgingList.as_view()),
    path('fol_stock_aging/<int:pk>/',
         views.FolStockAgingDetail.as_view()),

    path('fol_return_order_shipping_fee/',
         views.FolReturnOrderShippingFeeList.as_view()),
    path('fol_return_order_shipping_fee/<int:pk>/',
         views.FolReturnOrderShippingFeeDetail.as_view()),

    path('fol_return_order_item/',
         views.FolReturnOrderItemList.as_view()),
    path('fol_return_order_item/<int:pk>/',
         views.FolReturnOrderItemDetail.as_view()),

    path('fol_return_order/',
         views.FolReturnOrderList.as_view()),
    path('fol_return_order/<int:pk>/',
         views.FolReturnOrderDetail.as_view()),

    path('fol_order_shipping_fee/',
         views.FolOrderShippingFeeList.as_view()),
    path('fol_order_shipping_fee/<int:pk>/',
         views.FolOrderShippingFeeDetail.as_view()),

    path('fol_order_item/',
         views.FolOrderItemList.as_view()),
    path('fol_order_item/<int:pk>/',
         views.FolOrderItemDetail.as_view()),

    path('fol_order_fee/',
         views.FolOrderFeeList.as_view()),
    path('fol_order_fee/<int:pk>/',
         views.FolOrderFeeDetail.as_view()),

    path('fol_order_etc/',
         views.FolOrderEtcList.as_view()),
    path('fol_order_etc/<int:pk>/',
         views.FolOrderEtcDetail.as_view()),

    path('fol_order_base/',
         views.FolOrderBaseList.as_view()),
    path('fol_order_base/<int:pk>/',
         views.FolOrderBaseDetail.as_view()),

    #
    path('pro_return_order_shipping_fee/',
         views.ProReturnOrderShippingFeeList.as_view()),
    path('pro_return_order_shipping_fee/<int:pk>/',
         views.ProReturnOrderShippingFeeDetail.as_view()),

    path('pro_return_order_item/',
         views.ProReturnOrderItemList.as_view()),
    path('pro_return_order_item/<int:pk>/',
         views.ProReturnOrderItemDetail.as_view()),

    path('pro_return_order/',
         views.ProReturnOrderList.as_view()),
    path('pro_return_order/<int:pk>/',
         views.ProReturnOrderDetail.as_view()),

    path('pro_order_shipping_fee/',
         views.ProOrderShippingFeeList.as_view()),
    path('pro_order_shipping_fee/<int:pk>/',
         views.ProOrderShippingFeeDetail.as_view()),

    path('pro_order_item/',
         views.ProOrderItemList.as_view()),
    path('pro_order_item/<int:pk>/',
         views.ProOrderItemDetail.as_view()),

    path('pro_order_fee/',
         views.ProOrderFeeList.as_view()),
    path('pro_order_fee/<int:pk>/',
         views.ProOrderFeeDetail.as_view()),

    path('pro_order_etc/',
         views.ProOrderEtcList.as_view()),
    path('pro_order_etc/<int:pk>/',
         views.ProOrderEtcDetail.as_view()),

    path('pro_order_base/',
         views.ProOrderBaseList.as_view()),
    path('pro_order_base/<int:pk>/',
         views.ProOrderBaseDetail.as_view()),

    path('pro_products/', views.ProProductsList.as_view()),
    path('pro_products/<int:pk>/', views.ProProductsDetail.as_view()),

    path("fol_learn_dash/", views.FolLearnDashList.as_view()),
    path("fol_learn_dash/<int:pk>/", views.FolLearnDashDetail.as_view()),


]

urlpatterns = format_suffix_patterns(urlpatterns)
