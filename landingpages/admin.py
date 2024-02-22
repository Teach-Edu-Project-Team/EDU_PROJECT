from django.contrib import admin
from .models import *

# Register your models here.

class MaintenancePageAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enabled')
    
admin.site.register(MaintenancePage, MaintenancePageAdmin)