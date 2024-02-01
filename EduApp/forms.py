from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class PersonalForm(forms.ModelForm):
    
    class Meta:
        model = Personal
        exclude = ['user', 'profile_pic']
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            
        }
        

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['profile_pic']
        
class WorkForm(forms.ModelForm):
    class Meta:
        model= Work
        exclude = ['personal']
        widgets = {
            'date_of_appointment': forms.DateInput(attrs={'type': 'date'}),
            'date_at_current_station': forms.DateInput(attrs={'type': 'date'}),
            'date_promoted_to_rank': forms.DateInput(attrs={'type':'date'}),
            
        }
        
     
    def __init__(self, *args, **kwargs):
        super(WorkForm, self).__init__(*args, **kwargs)

        
        for field_name, field in self.fields.items():
            field.required = True
    
    
class NominalForm(forms.ModelForm):
    class Meta:
        model=Nominal
        exclude = ['personal']
           
    def __init__(self, *args, **kwargs):
        super(NominalForm, self).__init__(*args, **kwargs)

        
        for field_name, field in self.fields.items():
            field.required = True 
    
  
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username', 'email','password1', 'password2']
    