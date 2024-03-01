from django.shortcuts import render
from .forms import AccessForm
# Create your views here.
def  maintenanceview(request):
    return render(request, 'base.html')

def locekd_page(request):
    form = AccessForm()
    return render(request, 'locked.html', {'form': form})