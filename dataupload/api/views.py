from django.http import HttpResponse
from rest_framework import generics, permissions
from django.http import JsonResponse
import psycopg2
from rest_framework import viewsets

from . import models, serializers

conn = psycopg2.connect(dbname="defaultdb", user="doadmin",
                        password="AVNS_FovmirLSFDui0KIAOnu", host="db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com", port=25060)

#----------------------------------------------------GENERIC-------------------------------------------------------#


def TableNames(request):
    if request.method == 'GET':
        cur = conn.cursor()
        cur.execute(
            "select string_agg(table_name, ', ') from information_schema.tables where table_schema = 'public';")
        return JsonResponse(list(cur.fetchone())[0].split(", "), safe=False, json_dumps_params={'ensure_ascii': False})

# dataupload config

class TemplatesList(generics.ListCreateAPIView):
    queryset = models.DatauploadTabletemplates.objects.all()
    serializer_class = serializers.TemplatesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadTabletemplates.objects.all()
    serializer_class = serializers.TemplatesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SpecialQueriesList(generics.ListCreateAPIView):
    queryset = models.DatauploadImporttemplates.objects.all()
    serializer_class = serializers.ImportTemplatesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SpecialQueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadImporttemplates.objects.all()
    serializer_class = serializers.ImportTemplatesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UploadmodelViewSet(viewsets.ModelViewSet):
    queryset = models.DatauploadUploadmodel.objects.all()
    serializer_class = serializers.UploadModelSerializer

    def post(self, request, *args, **kwargs):
        table = request.data["table"]
        file = request.data["file"]
        user_id = request.data["table"]
        models.DatauploadUploadmodel.create(table=table, file=file, user_id=user_id)
        return HttpResponse({"message": "File uploaded"}, status=200)

# -------------------------------------------------- DATAS --------------------------------------------------------------- #
    # ------------------------------------------------FOL-------------------------------------------------------------#

# Fol Bevételek


class FolBevetelekList(generics.ListCreateAPIView):
    queryset = models.FolBevtelek.objects.all()
    serializer_class = serializers.FolBevetelekSerializer


class FolBevetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolBevtelek.objects.all()
    serializer_class = serializers.FolBevetelekSerializer


# Fol Költségek
class FolKoltsegekList(generics.ListCreateAPIView):
    queryset = models.FolKltsgek.objects.all()
    serializer_class = serializers.FolKoltsegekSerializer


class FolKoltsegDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolKltsgek.objects.all()
    serializer_class = serializers.FolKoltsegekSerializer

# Fol orders


class FolOrdersList(generics.ListCreateAPIView):
    queryset = models.FolOrders.objects.all()
    serializer_class = serializers.FolOrdersSerializer


class FolOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrders.objects.all()
    serializer_class = serializers.FolOrdersSerializer

# Fol product suppliers


class FolProductSuppliersList(generics.ListCreateAPIView):
    queryset = models.FolProductSuppliers.objects.all()
    serializer_class = serializers.FolProductSuppliersSerializer


class FolProductSupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolProductSuppliers.objects.all()
    serializer_class = serializers.FolProductSuppliersSerializer

# Fol stock report


class FolStockReportList(generics.ListCreateAPIView):
    queryset = models.FolStockReport.objects.all()
    serializer_class = serializers.FolStockReportSerializer


class FolStockReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolStockReport.objects.all()
    serializer_class = serializers.FolStockReportSerializer

# Fol számlák


class FolSzamlakList(generics.ListCreateAPIView):
    queryset = models.FolSzmlk.objects.all()
    serializer_class = serializers.FolSzamlakSerializer


class FolSzamlaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolSzmlk.objects.all()
    serializer_class = serializers.FolSzamlakSerializer

# Fol unas


class FolUnasList(generics.ListCreateAPIView):
    queryset = models.FolUnas.objects.all()
    serializer_class = serializers.FolUnasSerializer


class FolUnasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolUnas.objects.all()
    serializer_class = serializers.FolUnasSerializer


# Fol Gls elszámolás
class FolGlsElszámolásList(generics.ListCreateAPIView):
    queryset = models.FolGlsElszmols.objects.all()
    serializer_class = serializers.FolGlsElszámolsSerializer


class FolGlsElszámolásDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolGlsElszmols.objects.all()
    serializer_class = serializers.FolGlsElszámolsSerializer

    #------------------------------------------------PRO----------------------------------------------------------------#


class ProBevetelekList(generics.ListCreateAPIView):
    queryset = models.ProBevtelek.objects.all()
    serializer_class = serializers.ProBevetelekSerializer


class ProBevetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProBevtelek.objects.all()
    serializer_class = serializers.ProBevetelekSerializer


# Pro Költségek
class ProKoltsegekList(generics.ListCreateAPIView):
    queryset = models.ProKltsgek.objects.all()
    serializer_class = serializers.ProKoltsegekSerializer


class ProKoltsegDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProKltsgek.objects.all()
    serializer_class = serializers.ProKoltsegekSerializer

# Pro orders


class ProOrdersList(generics.ListCreateAPIView):
    queryset = models.ProOrders.objects.all()
    serializer_class = serializers.ProOrdersSerializer


class ProOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrders.objects.all()
    serializer_class = serializers.ProOrdersSerializer

# Pro product suppliers


class ProProductSuppliersList(generics.ListCreateAPIView):
    queryset = models.ProProductSuppliers.objects.all()
    serializer_class = serializers.ProProductSuppliersSerializer


class ProProductSupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProProductSuppliers.objects.all()
    serializer_class = serializers.ProProductSuppliersSerializer

# Pro stock report


class ProStockReportList(generics.ListCreateAPIView):
    queryset = models.ProStockReport.objects.all()
    serializer_class = serializers.ProStockReportSerializer


class ProStockReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProStockReport.objects.all()
    serializer_class = serializers.ProStockReportSerializer

# Pro számlák


class ProSzamlakList(generics.ListCreateAPIView):
    queryset = models.ProSzmlk.objects.all()
    serializer_class = serializers.ProSzamlakSerializer


class ProSzamlaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProSzmlk.objects.all()
    serializer_class = serializers.ProSzamlakSerializer
