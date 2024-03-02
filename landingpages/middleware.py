from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from .models import *

def maintenancepage_middleware(get_response):
    def middleware(request):
        
        if page_is_enabled('Maintenance'):     
            if request.path != reverse('maintenance'):
                if '/admin' not in request.path:
                    if settings.STAGING != 'True':
                        return HttpResponseRedirect(reverse('maintenance'))
        
        if page_is_enabled('Staging'):
            if request.path != reverse('locked'):
                if '/admin' not in request.path:
                    if settings.STAGING != 'True':
                        if 'staging_access' not in request.session:
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