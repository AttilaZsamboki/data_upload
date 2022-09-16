from http.client import HTTPResponse
from django.http import HttpResponse
from django.core.files import File
from rest_framework import generics
from django.http import JsonResponse
import psycopg2
from rest_framework import viewsets
from . import models, serializers
from .permissions import AuthorAllUser
from rest_framework.decorators import api_view
import os
import pandas as pd
from rest_framework.response import Response
from io import open


@api_view(["GET"])
def DownloadFile(request):
    if request.method == "GET":
        path_to_file = "/home/atti/googleds/files/" + request.GET.get("path")
        if os.path.exists(path_to_file):
            data = open(path_to_file, "rb")
            response = HttpResponse(
                File(data).read())
            response['Content-Disposition'] = 'attachment; filename=%s' % path_to_file.split(
                "/")[-1]
            return response
#----------------------------------------------------GENERIC-------------------------------------------------------#


def ColumnNames(request):
    conn = psycopg2.connect(dbname="defaultdb", user="doadmin",
                            password="AVNS_FovmirLSFDui0KIAOnu", host="db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com", port=25060)
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute(
            "select table_name, column_name, data_type from information_schema.columns where table_schema = 'public'")
        return JsonResponse((cur.fetchall()), safe=False, json_dumps_params={'ensure_ascii': False})
    cur.close()
    conn.close()


def TableNames(request):
    conn = psycopg2.connect(dbname="defaultdb", user="doadmin",
                            password="AVNS_FovmirLSFDui0KIAOnu", host="db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com", port=25060)
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute(
            "select string_agg(table_name, ', ') from information_schema.tables where table_schema = 'public';")
        return JsonResponse(list(cur.fetchone())[0].split(", "), safe=False, json_dumps_params={'ensure_ascii': False})
    cur.close()
    conn.close()

# dataupload config


class TemplatesList(generics.ListCreateAPIView):
    queryset = models.DatauploadTabletemplates.objects.all()
    serializer_class = serializers.TemplatesSerializer
    # permission_classes = [AuthorAllUser]


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadTabletemplates.objects.all()
    serializer_class = serializers.TemplatesSerializer
    permission_classes = [AuthorAllUser]


class UploadmodelList(generics.ListCreateAPIView):
    queryset = models.DatauploadUploadmodel.objects.all()
    serializer_class = serializers.UploadModelSerializer
    permission_classes = [AuthorAllUser]


class UploadmodelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadUploadmodel.objects.all()
    serializer_class = serializers.UploadModelSerializer
    permission_classes = [AuthorAllUser]


class TableOverviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadTableOverview.objects.all()
    serializer_class = serializers.TableoverviewSerializer
    permission_classes = [AuthorAllUser]


class TableOverviewList(generics.ListCreateAPIView):
    queryset = models.DatauploadTableOverview.objects.all()
    serializer_class = serializers.TableoverviewSerializer
    permission_classes = [AuthorAllUser]


# -------------------------------------------------- DATAS --------------------------------------------------------------- #
    # ------------------------------------------------FOL-------------------------------------------------------------#

# Fol Bevételek


class FolBevetelekList(generics.ListCreateAPIView):
    queryset = models.FolBevtelek.objects.all()
    serializer_class = serializers.FolBevetelekSerializer
    permission_classes = [AuthorAllUser]


class FolBevetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolBevtelek.objects.all()
    serializer_class = serializers.FolBevetelekSerializer
    permission_classes = [AuthorAllUser]


# Fol Költségek
class FolKoltsegekList(generics.ListCreateAPIView):
    queryset = models.FolKltsgek.objects.all()
    serializer_class = serializers.FolKoltsegekSerializer
    permission_classes = [AuthorAllUser]


class FolKoltsegDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolKltsgek.objects.all()
    serializer_class = serializers.FolKoltsegekSerializer
    permission_classes = [AuthorAllUser]

# Fol orders


class FolOrdersList(generics.ListCreateAPIView):
    queryset = models.FolOrders.objects.all()
    serializer_class = serializers.FolOrdersSerializer
    permission_classes = [AuthorAllUser]


class FolOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrders.objects.all()
    serializer_class = serializers.FolOrdersSerializer
    permission_classes = [AuthorAllUser]

# Fol product suppliers


class FolProductSuppliersList(generics.ListCreateAPIView):
    queryset = models.FolProductSuppliers.objects.all()
    serializer_class = serializers.FolProductSuppliersSerializer
    permission_classes = [AuthorAllUser]


class FolProductSupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolProductSuppliers.objects.all()
    serializer_class = serializers.FolProductSuppliersSerializer
    permission_classes = [AuthorAllUser]

# Fol stock report


class FolStockReportList(generics.ListCreateAPIView):
    queryset = models.FolStockReport.objects.all()
    serializer_class = serializers.FolStockReportSerializer
    permission_classes = [AuthorAllUser]


class FolStockReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolStockReport.objects.all()
    serializer_class = serializers.FolStockReportSerializer
    permission_classes = [AuthorAllUser]

# Fol számlák


class FolSzamlakList(generics.ListCreateAPIView):
    queryset = models.FolSzmlk.objects.all()
    serializer_class = serializers.FolSzamlakSerializer
    permission_classes = [AuthorAllUser]


class FolSzamlaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolSzmlk.objects.all()
    serializer_class = serializers.FolSzamlakSerializer
    permission_classes = [AuthorAllUser]

# Fol unas


class FolUnasList(generics.ListCreateAPIView):
    queryset = models.FolUnas.objects.all()
    serializer_class = serializers.FolUnasSerializer
    permission_classes = [AuthorAllUser]


class FolUnasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolUnas.objects.all()
    serializer_class = serializers.FolUnasSerializer
    permission_classes = [AuthorAllUser]


# Fol Gls elszámolás
class FolGlsElszámolásList(generics.ListCreateAPIView):
    queryset = models.FolGlsElszmols.objects.all()
    serializer_class = serializers.FolGlsElszámolsSerializer
    permission_classes = [AuthorAllUser]


class FolGlsElszámolásDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolGlsElszmols.objects.all()
    serializer_class = serializers.FolGlsElszámolsSerializer
    permission_classes = [AuthorAllUser]


class FolStockTransactionReportList(generics.ListCreateAPIView):
    queryset = models.FolStockTransactionReport.objects.all()
    serializer_class = serializers.FolStockTransactionReportSerializer
    permission_classes = [AuthorAllUser]


class FolStockTransactionReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolStockTransactionReport.objects.all()
    serializer_class = serializers.FolStockTransactionReportSerializer
    permission_classes = [AuthorAllUser]


class FolStockAgingList(generics.ListCreateAPIView):
    queryset = models.FolStockAging.objects.all()
    serializer_class = serializers.FolStockAgingSerializer
    permission_classes = [AuthorAllUser]


class FolReturnOrderShippingFeeList(generics.ListCreateAPIView):
    queryset = models.FolReturnOrderShippingFee.objects.all()
    serializer_class = serializers.FolReturnOrderShippingFeeSerializer
    permission_classes = [AuthorAllUser]


class FolReturnOrderItemList(generics.ListCreateAPIView):
    queryset = models.FolReturnOrderItem.objects.all()
    serializer_class = serializers.FolReturnOrderItemSerializer
    permission_classes = [AuthorAllUser]


class FolReturnOrderList(generics.ListCreateAPIView):
    queryset = models.FolReturnOrder.objects.all()
    serializer_class = serializers.FolReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class FolOrderShippingFeeList(generics.ListCreateAPIView):
    queryset = models.FolReturnOrder.objects.all()
    serializer_class = serializers.FolReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class FolOrderItemList(generics.ListCreateAPIView):
    queryset = models.FolOrderItem.objects.all()
    serializer_class = serializers.FolOrderItemSerializer
    permission_classes = [AuthorAllUser]


class FolOrderFeeList(generics.ListCreateAPIView):
    queryset = models.FolOrderFee.objects.all()
    serializer_class = serializers.FolOrderFeeSerializer
    permission_classes = [AuthorAllUser]


class FolOrderEtcList(generics.ListCreateAPIView):
    queryset = models.FolOrderEtc.objects.all()
    serializer_class = serializers.FolOrderEtcSerializer
    permission_classes = [AuthorAllUser]


class FolOrderBaseList(generics.ListCreateAPIView):
    queryset = models.FolOrderBase.objects.all()
    serializer_class = serializers.FolOrderBaseSerializer
    permission_classes = [AuthorAllUser]

#


class FolStockAgingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolStockAging.objects.all()
    serializer_class = serializers.FolStockAgingSerializer
    permission_classes = [AuthorAllUser]


class FolReturnOrderShippingFeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolReturnOrderShippingFee.objects.all()
    serializer_class = serializers.FolReturnOrderShippingFeeSerializer
    permission_classes = [AuthorAllUser]


class FolReturnOrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolReturnOrderItem.objects.all()
    serializer_class = serializers.FolReturnOrderItemSerializer
    permission_classes = [AuthorAllUser]


class FolReturnOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolReturnOrder.objects.all()
    serializer_class = serializers.FolReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class FolOrderShippingFeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolReturnOrder.objects.all()
    serializer_class = serializers.FolReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class FolOrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrderItem.objects.all()
    serializer_class = serializers.FolOrderItemSerializer
    permission_classes = [AuthorAllUser]


class FolOrderFeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrderFee.objects.all()
    serializer_class = serializers.FolOrderFeeSerializer
    permission_classes = [AuthorAllUser]


class FolOrderEtcDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrderEtc.objects.all()
    serializer_class = serializers.FolOrderEtcSerializer
    permission_classes = [AuthorAllUser]


class FolOrderBaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrderBase.objects.all()
    serializer_class = serializers.FolOrderBaseSerializer
    permission_classes = [AuthorAllUser]

    #------------------------------------------------PRO----------------------------------------------------------------#


class ProBevetelekList(generics.ListCreateAPIView):
    queryset = models.ProBevtelek.objects.all()
    serializer_class = serializers.ProBevetelekSerializer
    permission_classes = [AuthorAllUser]


class ProBevetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProBevtelek.objects.all()
    serializer_class = serializers.ProBevetelekSerializer
    permission_classes = [AuthorAllUser]


# Pro Költségek
class ProKoltsegekList(generics.ListCreateAPIView):
    queryset = models.ProKltsgek.objects.all()
    serializer_class = serializers.ProKoltsegekSerializer
    permission_classes = [AuthorAllUser]


class ProKoltsegDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProKltsgek.objects.all()
    serializer_class = serializers.ProKoltsegekSerializer
    permission_classes = [AuthorAllUser]

# Pro orders


class ProOrdersList(generics.ListCreateAPIView):
    queryset = models.ProOrders.objects.all()
    serializer_class = serializers.ProOrdersSerializer
    permission_classes = [AuthorAllUser]


class ProOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrders.objects.all()
    serializer_class = serializers.ProOrdersSerializer
    permission_classes = [AuthorAllUser]

# Pro product suppliers


class ProProductSuppliersList(generics.ListCreateAPIView):
    queryset = models.ProProductSuppliers.objects.all()
    serializer_class = serializers.ProProductSuppliersSerializer
    permission_classes = [AuthorAllUser]


class ProProductSupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProProductSuppliers.objects.all()
    serializer_class = serializers.ProProductSuppliersSerializer
    permission_classes = [AuthorAllUser]

# Pro stock report


class ProStockReportList(generics.ListCreateAPIView):
    queryset = models.ProStockReport.objects.all()
    serializer_class = serializers.ProStockReportSerializer
    permission_classes = [AuthorAllUser]


class ProStockReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProStockReport.objects.all()
    serializer_class = serializers.ProStockReportSerializer
    permission_classes = [AuthorAllUser]

# Pro számlák


class ProSzamlakList(generics.ListCreateAPIView):
    queryset = models.ProSzmlk.objects.all()
    serializer_class = serializers.ProSzamlakSerializer
    permission_classes = [AuthorAllUser]


class ProSzamlaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProSzmlk.objects.all()
    serializer_class = serializers.ProSzamlakSerializer
    permission_classes = [AuthorAllUser]


class ProStockTransactionReportList(generics.ListCreateAPIView):
    queryset = models.ProStockTransactionReport.objects.all()
    serializer_class = serializers.ProStockTransactionReportSerializer
    permission_classes = [AuthorAllUser]


class ProStockTransactionReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProStockTransactionReport.objects.all()
    serializer_class = serializers.ProStockTransactionReportSerializer
    permission_classes = [AuthorAllUser]


class ProStockAgingList(generics.ListCreateAPIView):
    queryset = models.ProStockAging.objects.all()
    serializer_class = serializers.ProStockAgingSerializer
    permission_classes = [AuthorAllUser]


class ProReturnOrderShippingFeeList(generics.ListCreateAPIView):
    queryset = models.ProReturnOrderShippingFee.objects.all()
    serializer_class = serializers.ProReturnOrderShippingFeeSerializer
    permission_classes = [AuthorAllUser]


class ProReturnOrderItemList(generics.ListCreateAPIView):
    queryset = models.ProReturnOrderItem.objects.all()
    serializer_class = serializers.ProReturnOrderItemSerializer
    permission_classes = [AuthorAllUser]


class ProReturnOrderList(generics.ListCreateAPIView):
    queryset = models.ProReturnOrder.objects.all()
    serializer_class = serializers.ProReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class ProOrderShippingFeeList(generics.ListCreateAPIView):
    queryset = models.ProReturnOrder.objects.all()
    serializer_class = serializers.ProReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class ProOrderItemList(generics.ListCreateAPIView):
    queryset = models.ProOrderItem.objects.all()
    serializer_class = serializers.ProOrderItemSerializer
    permission_classes = [AuthorAllUser]


class ProOrderFeeList(generics.ListCreateAPIView):
    queryset = models.ProOrderFee.objects.all()
    serializer_class = serializers.ProOrderFeeSerializer
    permission_classes = [AuthorAllUser]


class ProOrderEtcList(generics.ListCreateAPIView):
    queryset = models.ProOrderEtc.objects.all()
    serializer_class = serializers.ProOrderEtcSerializer
    permission_classes = [AuthorAllUser]


class ProOrderBaseList(generics.ListCreateAPIView):
    queryset = models.ProOrderBase.objects.all()
    serializer_class = serializers.ProOrderBaseSerializer
    permission_classes = [AuthorAllUser]

#


class ProStockAgingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProStockAging.objects.all()
    serializer_class = serializers.ProStockAgingSerializer
    permission_classes = [AuthorAllUser]


class ProReturnOrderShippingFeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProReturnOrderShippingFee.objects.all()
    serializer_class = serializers.ProReturnOrderShippingFeeSerializer
    permission_classes = [AuthorAllUser]


class ProReturnOrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProReturnOrderItem.objects.all()
    serializer_class = serializers.ProReturnOrderItemSerializer
    permission_classes = [AuthorAllUser]


class ProReturnOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProReturnOrder.objects.all()
    serializer_class = serializers.ProReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class ProOrderShippingFeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProReturnOrder.objects.all()
    serializer_class = serializers.ProReturnOrderSerializer
    permission_classes = [AuthorAllUser]


class ProOrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrderItem.objects.all()
    serializer_class = serializers.ProOrderItemSerializer
    permission_classes = [AuthorAllUser]


class ProOrderFeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrderFee.objects.all()
    serializer_class = serializers.ProOrderFeeSerializer
    permission_classes = [AuthorAllUser]


class ProOrderEtcDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrderEtc.objects.all()
    serializer_class = serializers.ProOrderEtcSerializer
    permission_classes = [AuthorAllUser]


class ProOrderBaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrderBase.objects.all()
    serializer_class = serializers.ProOrderBaseSerializer
    permission_classes = [AuthorAllUser]


class ProProductsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProProducts.objects.all()
    serializer_class = serializers.ProProductsSerializer
    permission_classes = [AuthorAllUser]


class ProProductsList(generics.ListCreateAPIView):
    queryset = models.ProProducts.objects.all()
    serializer_class = serializers.ProProductsSerializer
    permission_classes = [AuthorAllUser]


class ProProductsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProProducts.objects.all()
    serializer_class = serializers.ProProductsSerializer
    permission_classes = [AuthorAllUser]


class ProProductsList(generics.ListCreateAPIView):
    queryset = models.ProProducts.objects.all()
    serializer_class = serializers.ProProductsSerializer
    permission_classes = [AuthorAllUser]


class FolLearnDashDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolLearnDash.objects.all()
    serializer_class = serializers.FolLearnDashSerializer
    permission_classes = [AuthorAllUser]


class FolLearnDashList(generics.ListCreateAPIView):
    queryset = models.FolLearnDash.objects.all()
    serializer_class = serializers.FolLearnDashSerializer
    permission_classes = [AuthorAllUser]


class FeedDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Feed.objects.all()
    serializer_class = serializers.FeedSerializer
    permission_classes = [AuthorAllUser]


class FeedList(generics.ListCreateAPIView):
    queryset = models.Feed.objects.all()
    serializer_class = serializers.FeedSerializer
    permission_classes = [AuthorAllUser]
