from django.contrib import admin
from .models import Role, User, Permission, RolePermission


admin.site.register(Role)
admin.site.register(User)
admin.site.register(Permission)
admin.site.register(RolePermission)