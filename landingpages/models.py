from django.db import models

# Create your models here.
class MaintenancePage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.name)  
    
    class Meta:
        ordering = ['name']  