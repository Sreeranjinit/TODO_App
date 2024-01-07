from django import forms
from django.contrib.auth.models import User
from ToDo_App.models import Task



class registerform(forms.ModelForm):
    class Meta:   
        model=User
        fields=['username','password','first_name','last_name','email']
        

class signin(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class  taskform(forms.ModelForm):
    class Meta:
        model=Task
        fields=['Name']

    
