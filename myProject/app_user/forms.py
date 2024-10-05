from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myQuataWeb.models import Student

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] 

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'faculty', 'profile_pic']


