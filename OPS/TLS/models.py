from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "documents/%s/%s" %(instance.user.id, filename)
    #return 'documents/user_{0}/'.format(instance.user.id)

class Document(models.Model):
    #user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    #document = models.FileField(upload_to='documents/{user_id}/', null=True, blank=False )
    document = models.FileField(upload_to=user_directory_path, null=True, blank=False )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


"""from django.db import models

class Document(models.Model):
    #document = models.FileField(upload_to='documents/%Y/%m/%d/'', null=True, blank=False )
    document = models.FileField(upload_to='documents/%Y/%m/%d/', null=True, blank=False )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
"""
