from EduApp.models import *

def run():
    personal = Personal.objects.all()
    
    print(personal.work_set.all())
    

   