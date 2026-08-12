import uuid
from django.db import models
from django.conf import settings


# Records who did what, when, to which record. Uses a generic reference
class AuditTrail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='audit_entries')
    action = models.CharField(max_length=100)  # e.g. "CREATE", "APPROVE", "DELETE"
    entity_type = models.CharField(max_length=100)  # e.g. "PurchaseOrder"
    entity_id = models.UUIDField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.entity_type} at {self.timestamp}"