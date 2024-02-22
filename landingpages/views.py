from django.shortcuts import render

# Create your views here.
def  maintenanceview(request):
    return render(request, 'base.html')

def locekd_page(request):
    return render(request, 'locked.html')