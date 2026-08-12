from rest_framework import viewsets
from .models import ItemCategory, Item, Supplier, ItemSupplier
from .serializers import ItemCategorySerializer, ItemSerializer, SupplierSerializer, ItemSupplierSerializer


class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ItemSupplierViewSet(viewsets.ModelViewSet):
    queryset = ItemSupplier.objects.all()
    serializer_class = ItemSupplierSerializer