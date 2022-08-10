from http.client import HTTPResponse
from django.shortcuts import redirect
from rest_framework import generics
from django.http import JsonResponse
import psycopg2
from rest_framework import viewsets, authentication, exceptions
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from . import models, serializers

conn = psycopg2.connect(dbname="defaultdb", user="doadmin",
                        password="AVNS_FovmirLSFDui0KIAOnu", host="db-postgresql-fra1-91708-jun-25-backup-do-user-4907952-0.b.db.ondigitalocean.com", port=25060)

#----------------------------------------------------GENERIC-------------------------------------------------------#
class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.COOKIES['id.6nz455rn'].username
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)


def ColumnNames(request):
    try:
        access_cookie = request.COOKIES['id.6nz455rn']
    except:
        access_cookie = ""
        return redirect("http://127.0.0.1:8000/login")
    if access_cookie:
        if request.method == 'GET':
            cur = conn.cursor()
            cur.execute(
                "select table_name, column_name from information_schema.columns where table_schema = 'public'")
            return JsonResponse((cur.fetchall()), safe=False, json_dumps_params={'ensure_ascii': False})


def TableNames(request):
    try:
        access_cookie = request.COOKIES['access.6nz455rn']
    except:
        access_cookie = ""
        return redirect("http://127.0.0.1:8000/login")
    if access_cookie:
        if request.method == 'GET':
            cur = conn.cursor()
            cur.execute(
                "select string_agg(table_name, ', ') from information_schema.tables where table_schema = 'public';")
            return JsonResponse(list(cur.fetchone())[0].split(", "), safe=False, json_dumps_params={'ensure_ascii': False})

# dataupload config


class TemplatesList(generics.ListCreateAPIView):
    queryset = models.DatauploadTabletemplates.objects.all()
    serializer_class = serializers.TemplatesSerializer
    permission_classes = [IsAuthenticated]


class TemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadTabletemplates.objects.all()
    serializer_class = serializers.TemplatesSerializer
    permission_classes = [IsAuthenticated]


class SpecialQueriesList(generics.ListCreateAPIView):
    queryset = models.DatauploadImporttemplates.objects.all()
    serializer_class = serializers.ImportTemplatesSerializer
    permission_classes = [IsAuthenticated]


class SpecialQueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DatauploadImporttemplates.objects.all()
    serializer_class = serializers.ImportTemplatesSerializer
    permission_classes = [IsAuthenticated]



class UploadmodelViewSet(viewsets.ModelViewSet):
    queryset = models.DatauploadUploadmodel.objects.all()
    serializer_class = serializers.UploadModelSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        table = request.data["table"]
        file = request.data["file"]
        user_id = request.data["table"]
        models.DatauploadUploadmodel.create(
            table=table, file=file, user_id=user_id)
        return HTTPResponse({"message": "File uploaded"}, status=200)

# -------------------------------------------------- DATAS --------------------------------------------------------------- #
    # ------------------------------------------------FOL-------------------------------------------------------------#

# Fol Bevételek


class FolBevetelekList(generics.ListCreateAPIView):
    queryset = models.FolBevtelek.objects.all()
    serializer_class = serializers.FolBevetelekSerializer
    permission_classes = [IsAuthenticated]


class FolBevetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolBevtelek.objects.all()
    serializer_class = serializers.FolBevetelekSerializer
    permission_classes = [IsAuthenticated]


# Fol Költségek
class FolKoltsegekList(generics.ListCreateAPIView):
    queryset = models.FolKltsgek.objects.all()
    serializer_class = serializers.FolKoltsegekSerializer
    permission_classes = [IsAuthenticated]


class FolKoltsegDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolKltsgek.objects.all()
    serializer_class = serializers.FolKoltsegekSerializer
    permission_classes = [IsAuthenticated]

# Fol orders


class FolOrdersList(generics.ListCreateAPIView):
    queryset = models.FolOrders.objects.all()
    serializer_class = serializers.FolOrdersSerializer
    permission_classes = [IsAuthenticated]


class FolOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolOrders.objects.all()
    serializer_class = serializers.FolOrdersSerializer
    permission_classes = [IsAuthenticated]

# Fol product suppliers


class FolProductSuppliersList(generics.ListCreateAPIView):
    queryset = models.FolProductSuppliers.objects.all()
    serializer_class = serializers.FolProductSuppliersSerializer
    permission_classes = [IsAuthenticated]


class FolProductSupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolProductSuppliers.objects.all()
    serializer_class = serializers.FolProductSuppliersSerializer
    permission_classes = [IsAuthenticated]

# Fol stock report


class FolStockReportList(generics.ListCreateAPIView):
    queryset = models.FolStockReport.objects.all()
    serializer_class = serializers.FolStockReportSerializer
    permission_classes = [IsAuthenticated]


class FolStockReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolStockReport.objects.all()
    serializer_class = serializers.FolStockReportSerializer
    permission_classes = [IsAuthenticated]

# Fol számlák


class FolSzamlakList(generics.ListCreateAPIView):
    queryset = models.FolSzmlk.objects.all()
    serializer_class = serializers.FolSzamlakSerializer
    permission_classes = [IsAuthenticated]


class FolSzamlaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolSzmlk.objects.all()
    serializer_class = serializers.FolSzamlakSerializer
    permission_classes = [IsAuthenticated]

# Fol unas


class FolUnasList(generics.ListCreateAPIView):
    queryset = models.FolUnas.objects.all()
    serializer_class = serializers.FolUnasSerializer
    permission_classes = [IsAuthenticated]


class FolUnasDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolUnas.objects.all()
    serializer_class = serializers.FolUnasSerializer
    permission_classes = [IsAuthenticated]


# Fol Gls elszámolás
class FolGlsElszámolásList(generics.ListCreateAPIView):
    queryset = models.FolGlsElszmols.objects.all()
    serializer_class = serializers.FolGlsElszámolsSerializer
    permission_classes = [IsAuthenticated]

class FolGlsElszámolásDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.FolGlsElszmols.objects.all()
    serializer_class = serializers.FolGlsElszámolsSerializer
    permission_classes = [IsAuthenticated]

    #------------------------------------------------PRO----------------------------------------------------------------#


class ProBevetelekList(generics.ListCreateAPIView):
    queryset = models.ProBevtelek.objects.all()
    serializer_class = serializers.ProBevetelekSerializer
    permission_classes = [IsAuthenticated]


class ProBevetelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProBevtelek.objects.all()
    serializer_class = serializers.ProBevetelekSerializer
    permission_classes = [IsAuthenticated]


# Pro Költségek
class ProKoltsegekList(generics.ListCreateAPIView):
    queryset = models.ProKltsgek.objects.all()
    serializer_class = serializers.ProKoltsegekSerializer
    permission_classes = [IsAuthenticated]


class ProKoltsegDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProKltsgek.objects.all()
    serializer_class = serializers.ProKoltsegekSerializer
    permission_classes = [IsAuthenticated]

# Pro orders


class ProOrdersList(generics.ListCreateAPIView):
    queryset = models.ProOrders.objects.all()
    serializer_class = serializers.ProOrdersSerializer
    permission_classes = [IsAuthenticated]


class ProOrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProOrders.objects.all()
    serializer_class = serializers.ProOrdersSerializer
    permission_classes = [IsAuthenticated]

# Pro product suppliers


class ProProductSuppliersList(generics.ListCreateAPIView):
    queryset = models.ProProductSuppliers.objects.all()
    serializer_class = serializers.ProProductSuppliersSerializer
    permission_classes = [IsAuthenticated]


class ProProductSupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProProductSuppliers.objects.all()
    serializer_class = serializers.ProProductSuppliersSerializer
    permission_classes = [IsAuthenticated]

# Pro stock report


class ProStockReportList(generics.ListCreateAPIView):
    queryset = models.ProStockReport.objects.all()
    serializer_class = serializers.ProStockReportSerializer
    permission_classes = [IsAuthenticated]


class ProStockReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProStockReport.objects.all()
    serializer_class = serializers.ProStockReportSerializer
    permission_classes = [IsAuthenticated]

# Pro számlák


class ProSzamlakList(generics.ListCreateAPIView):
    queryset = models.ProSzmlk.objects.all()
    serializer_class = serializers.ProSzamlakSerializer
    permission_classes = [IsAuthenticated]


class ProSzamlaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProSzmlk.objects.all()
    serializer_class = serializers.ProSzamlakSerializer
    permission_classes = [IsAuthenticated]
