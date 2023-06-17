from django.db import models
from django import forms
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
# Create your models here.

# Registration Model
class Register (models.Model):
    name = models.CharField("Name",max_length=100)
    email = models.EmailField("Email",max_length=100)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)

    def __str__(self):
        return self.name

# Login Model 
class Login(models.Model):
    email = models.EmailField("Email",max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email



# View Model

class File(models.Model):
    ACCESS_CHOICES = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    )

    name = models.CharField("Name", max_length=100)
    file = models.FileField(upload_to='files/', validators=[FileExtensionValidator(['mp3'])])
    uploader = models.ForeignKey(Login, on_delete=models.CASCADE)
    access_type = models.CharField(choices=ACCESS_CHOICES, default='private', max_length=10)

    def __str__(self):
        return self.name

# class File(models.Model):
#     PUBLIC = 'public'
#     PRIVATE = 'private'
#     PROTECTED = 'protected'
#     ACCESS_CHOICES = (
#         (PUBLIC, 'Public'),
#         (PRIVATE, 'Private'),
#         (PROTECTED, 'Protected'),
#     )

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     file = models.FileField(upload_to='music_files/')
#     access = models.CharField(max_length=10, choices=ACCESS_CHOICES)
#     allowed_emails = models.TextField(blank=True)

#     def __str__(self):
#         return self.title

