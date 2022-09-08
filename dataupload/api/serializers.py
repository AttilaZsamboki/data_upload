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

class TableoverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatauploadTableOverview
        fields = '__all__'

# datas serializers
# FOl


class FolReturnOrderShippingFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolReturnOrderShippingFee
        fields = '__all__'


class FolReturnOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolReturnOrderItem
        fields = '__all__'


class FolReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolReturnOrder
        fields = '__all__'


class FolOrderShippingFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolOrderShippingFee
        fields = '__all__'


class FolOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolOrderItem
        fields = '__all__'


class FolOrderFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolOrderFee
        fields = '__all__'


class FolOrderEtcSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolOrderEtc
        fields = '__all__'


class FolOrderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolOrderBase
        fields = '__all__'


class FolStockTransactionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolStockTransactionReport
        fields = '__all__'


class FolStockAgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolStockAging
        fields = '__all__'


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


class ProReturnOrderShippingFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProReturnOrderShippingFee
        fields = '__all__'


class ProReturnOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProReturnOrderItem
        fields = '__all__'


class ProReturnOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProReturnOrder
        fields = '__all__'


class ProOrderShippingFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProOrderShippingFee
        fields = '__all__'


class ProOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProOrderItem
        fields = '__all__'


class ProOrderFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProOrderFee
        fields = '__all__'


class ProOrderEtcSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProOrderEtc
        fields = '__all__'


class ProOrderBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProOrderBase
        fields = '__all__'


class ProStockTransactionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProStockTransactionReport
        fields = '__all__'


class ProStockAgingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProStockAging
        fields = '__all__'


class ProProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProProducts
        fields = '__all__'
