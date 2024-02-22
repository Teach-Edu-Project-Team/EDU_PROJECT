from django.urls import path
from .views import *

urlpatterns = [
    path('maintenance/', maintenanceview, name='maintenance'),
    path('locked/', locekd_page, name='locked'),
    
]