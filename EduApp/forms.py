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

class NominalForm(forms.ModelForm):
    class Meta:
        model=Nominal
        exclude = ['personal']
        
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields=['username', 'email','password1', 'password2']
    