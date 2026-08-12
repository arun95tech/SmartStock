from rest_framework import viewsets
from .models import PurchaseOrder, POLine, GoodsReceipt, GRLine, QCHold
from .serializers import PurchaseOrderSerializer, POLineSerializer, GoodsReceiptSerializer, GRLineSerializer, QCHoldSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class POLineViewSet(viewsets.ModelViewSet):
    queryset = POLine.objects.all()
    serializer_class = POLineSerializer


class GoodsReceiptViewSet(viewsets.ModelViewSet):
    queryset = GoodsReceipt.objects.all()
    serializer_class = GoodsReceiptSerializer


class GRLineViewSet(viewsets.ModelViewSet):
    queryset = GRLine.objects.all()
    serializer_class = GRLineSerializer


class QCHoldViewSet(viewsets.ModelViewSet):
    queryset = QCHold.objects.all()
    serializer_class = QCHoldSerializer