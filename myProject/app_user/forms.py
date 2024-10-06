from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myQuataWeb.models import Student

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'faculty', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Faculty'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
