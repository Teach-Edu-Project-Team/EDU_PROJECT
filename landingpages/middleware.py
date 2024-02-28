from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .models import *

def maintenancepage_middleware(get_response):
    def middleware(request):
        
        if page_is_enabled('Maintenance'):     
            if request.path != reverse('maintenance'):
                if '/admin' not in request.path:
                    if settings.STAGING != 'False':
                        return HttpResponseRedirect(reverse('maintenance'))
        
        
        response = get_response(request)    
        return response
    
    return middleware

def page_is_enabled(page_name):
    page = MaintenancePage.objects.filter(name = page_name).first()
    if page:
        return page.is_enabled
    else:
        return False