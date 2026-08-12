from rest_framework import serializers
from .models import PurchaseOrder, POLine, GoodsReceipt, GRLine, QCHold


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class POLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = POLine
        fields = '__all__'


class GoodsReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceipt
        fields = '__all__'


class GRLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = GRLine
        fields = '__all__'


class QCHoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = QCHold
        fields = '__all__'