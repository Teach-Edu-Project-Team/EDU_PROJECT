import django_filters
from .models import Personal

class PersonalFilter(django_filters.FilterSet):
    class Meta:
        model = Personal
        fields= ['first_name', 'last_name',]
        
    def exclude_admin_users(self, queryset, name, value):
        return queryset.exclude(user__is_staff=True, user__is_superuser=True)