from rest_framework import viewsets
from .models import AuditTrail
from .serializers import AuditTrailSerializer


class AuditTrailViewSet(viewsets.ModelViewSet):
    queryset = AuditTrail.objects.all()
    serializer_class = AuditTrailSerializer