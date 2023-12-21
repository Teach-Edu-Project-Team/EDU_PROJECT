# your_app/templatetags/custom_tags.py
from django import template
from EduApp.models import Work, Personal

register = template.Library()

@register.simple_tag
def staff_category(personal_instance):
    try:
        work_instance = Work.objects.get(personal=personal_instance)
        return work_instance.staff_category
    except Work.DoesNotExist:
        return "N/A"
    
@register.simple_tag
def count_teaching_staff():
    return Work.objects.filter(staff_category='Teaching staff').count()

@register.simple_tag
def count_non_teaching_staff():
    return Work.objects.filter(staff_category='Non teaching staff').count()


@register.simple_tag
def get_personal_info(user):
    try:
        personal_info = Personal.objects.get(email=user.email)
        return personal_info
    except Personal.DoesNotExist:
        return None
