from .models import Register, Login, File
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Registration Form
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['name','email','password','confirm_password']
        widgets = { 'password': forms.PasswordInput(), 'confirm_password': forms.PasswordInput() }


# Login Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['email','password']
        widgets = { 'password': forms.PasswordInput() }

# File Upload Form
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name','file','uploader','access_type']


