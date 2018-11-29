from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Role)


class PermissionConfig(admin.ModelAdmin):
    list_display = ["title","url","p_group","code"]
admin.site.register(Permission,PermissionConfig)
admin.site.register(PermissionGroup)