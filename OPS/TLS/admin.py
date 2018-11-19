from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UploadData
admin.site.register(UploadData)

from .models import psqlUpload
admin.site.register(psqlUpload)

# Register your models here.
