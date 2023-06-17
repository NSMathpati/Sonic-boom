from django.contrib import admin
from .models import Register, Login, File
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
# Register your models here.

admin.site.register(Register)
admin.site.register(Login)
admin.site.register(File)
