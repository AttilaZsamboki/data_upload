from . import models
from rest_framework import serializers


# database config serializers
class DatabaseConnectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatauploadDatabaseconnections
        fields = '__all__'


class UploadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatauploadUploadmodel
        fields = '__all__'


class ImportTemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatauploadImporttemplates
        fields = '__all__'


class TemplatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatauploadTabletemplates
        fields = '__all__'

# datas serializers
# FOl


class FolBevetelekSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.FolBevtelek
        fields = '__all__'


class FolKoltsegekSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolKltsgek
        fields = '__all__'


class FolOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolOrders
        fields = '__all__'


class FolProductSuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolProductSuppliers
        fields = '__all__'


class FolStockReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolStockReport
        fields = '__all__'


class FolSzamlakSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolSzmlk
        fields = '__all__'


class FolUnasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolUnas
        fields = '__all__'


class FolGlsElszámolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolGlsElszmols
        fields = '__all__'

# PRO


class ProBevetelekSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.ProBevtelek
        fields = '__all__'


class ProKoltsegekSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProKltsgek
        fields = '__all__'


class ProOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProOrders
        fields = '__all__'


class ProProductSuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProProductSuppliers
        fields = '__all__'


class ProStockReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProStockReport
        fields = '__all__'


class ProSzamlakSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProSzmlk
        fields = '__all__'
