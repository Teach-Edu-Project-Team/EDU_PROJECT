import django_filters
from .models import Personal

class PersonalFilter(django_filters.FilterSet):
    class Meta:
        model = Personal
        fields= ['first_name', 'last_name',]