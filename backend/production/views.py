from rest_framework import viewsets
from .models import BOMHeader, BOMLine, WorkOrder, MaterialReservation, MaterialIssue, FGReceipt
from .serializers import BOMHeaderSerializer, BOMLineSerializer, WorkOrderSerializer, MaterialReservationSerializer, MaterialIssueSerializer, FGReceiptSerializer


class BOMHeaderViewSet(viewsets.ModelViewSet):
    queryset = BOMHeader.objects.all()
    serializer_class = BOMHeaderSerializer


class BOMLineViewSet(viewsets.ModelViewSet):
    queryset = BOMLine.objects.all()
    serializer_class = BOMLineSerializer


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer


class MaterialReservationViewSet(viewsets.ModelViewSet):
    queryset = MaterialReservation.objects.all()
    serializer_class = MaterialReservationSerializer


class MaterialIssueViewSet(viewsets.ModelViewSet):
    queryset = MaterialIssue.objects.all()
    serializer_class = MaterialIssueSerializer


class FGReceiptViewSet(viewsets.ModelViewSet):
    queryset = FGReceipt.objects.all()
    serializer_class = FGReceiptSerializer