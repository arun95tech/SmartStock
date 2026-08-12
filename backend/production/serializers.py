from rest_framework import serializers
from .models import BOMHeader, BOMLine, WorkOrder, MaterialReservation, MaterialIssue, FGReceipt


class BOMHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMHeader
        fields = '__all__'


class BOMLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BOMLine
        fields = '__all__'


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'


class MaterialReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialReservation
        fields = '__all__'


class MaterialIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialIssue
        fields = '__all__'
        read_only_fields = ['id', 'issue_date']


class FGReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FGReceipt
        fields = '__all__'