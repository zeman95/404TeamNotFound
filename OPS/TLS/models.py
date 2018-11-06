from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "documents/%s/%s" %(instance.user.id, filename)
    #return 'documents/user_{0}/'.format(instance.user.id)

def validate_file_extension(filename):
  import os
  ext = os.path.splitext(filename.name)[1]
  valid_extensions = ['.pdf','.doc','.docx']
  if not ext in valid_extensions:
    raise ValidationError(u'File {0} not supported!'.format(filename))

class Document(models.Model):
    #user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    #document = models.FileField(upload_to='documents/{user_id}/', null=True, blank=False )
    document = models.FileField(upload_to=user_directory_path, null=True, blank=False, validators=[validate_file_extension] )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


"""from django.db import models

class Document(models.Model):
    #document = models.FileField(upload_to='documents/%Y/%m/%d/'', null=True, blank=False )
    document = models.FileField(upload_to='documents/%Y/%m/%d/', null=True, blank=False )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
"""
