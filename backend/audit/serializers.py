from rest_framework import serializers
from .models import AuditTrail


class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']