import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission as AuthPermission
from django.db import models


# Role = one of the 5 job roles (Admin, Purchasing Officer, etc.)
class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Custom User model. We extend Django's AbstractUser instead of
# writing our own from scratch, because AbstractUser already handles
# password hashing and login securely.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)

    # groups/user_permissions need a unique related_name here because
    # Django's own default User model also defines these two fields,
    # and both models exist in the project at the same time.
    groups = models.ManyToManyField(Group, related_name='accounts_user_set', blank=True)
    user_permissions = models.ManyToManyField(AuthPermission, related_name='accounts_user_set', blank=True)

    def __str__(self):
        return self.username


# One specific permission, e.g. "can_approve_purchase_order"
# (Our own RBAC table — separate from Django's built-in Permission model above.)
class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code


# Links roles to permissions (many-to-many)
class RolePermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')