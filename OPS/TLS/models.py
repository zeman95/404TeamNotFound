from django.db import models
from django.contrib.auth.models import User
from users.models import CustomUser 
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
#from docx import Document
#from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crum import get_current_user

# try to import fields from postgres
from django.contrib.postgres.fields import ArrayField


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/user_<id>/<filename>
    currUser = get_current_user()
    
    
    #if instance.count >= 1:
    #    instance.count +=1
    #    instance.save()
    #    currUser.incUploads()
    #    currUser.save()
    #currUser.incUploads()
    #currUser.save()
    currentUpload = currUser.getUploads()#CustomUser.objects.get(currUser.id)
    #return "documents/%s/%s" %(instance.user.id, filename)
    return "documents/%s/%s/%s" %(currUser.id, currentUpload, filename)

#from django.core.exceptions import ValidationError
def validate_file_extension(filename):
  import os
  ext = os.path.splitext(filename.name)[1]
  valid_extensions = ['.pdf','.doc','.docx']
  if not ext in valid_extensions:
    raise ValidationError(u'File {0} not supported!'.format(filename))

class Document(models.Model):
    #document = models.FileField(upload_to=user_directory_path, null=True, blank=False, validators=[validate_file_extension] )
    description = models.CharField(max_length=255, blank=True)
    #uploaded_at = models.DateTimeField(auto_now_add=True)


"""class Attachment(models.Model):
    file = models.FileField(upload_to='documents/')"""


class UploadData(models.Model):
    grade = models.CharField(max_length=255, blank=False)
    req = models.CharField(max_length=255, blank=False)
    uploadNum = models.CharField(max_length=255, blank=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, null=False)
    uploadPath = models.CharField(max_length=512, blank=False)
    numberOfFiles = models.CharField(max_length=512, blank=False)
    userID = models.CharField(max_length=512, blank=False)
    filenames = models.CharField(max_length=3000, blank=False)



class Message(models.Model):
    author_name = models.CharField(_('Name'), max_length=255)
    author_email = models.EmailField(_('Email'))
    content = models.TextField(_('Content'))
    #description = models.CharField(max_length=255, blank=True, null=True)


class Attachment(models.Model):
    message = models.ForeignKey(Message, verbose_name=_('Message'), on_delete=models.CASCADE, null=True)
    file = models.FileField(_('Attachment'), upload_to=user_directory_path)
    count = models.IntegerField(default=0)


class PSQLUpload(models.Model):
    #user_id = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, null=False)
    userID = models.CharField(max_length=512, blank=False)
    filename = models.CharField(max_length=255, blank=False)
    uploadNumber = models.CharField(max_length=255, blank=False)
    reqTestedOn = models.CharField(max_length=512, blank=False)
    #querystring = models.TextField(blank=False)
    queryArraySize = models.CharField(max_length=512, blank=False)
    queryArray = ArrayField(models.TextField(blank=True)) # this is a dynamically created array that will store all the teachers lesson plan 'body' content
    #resultantArray = ArrayField(models.ForeignKey(Resultants, on_delete=models.CASCADE), blank=True)
    querysearch = models.CharField(max_length=3000, blank=False) #models.TextField(blank=True)
    #search_vector = SearchVectorField(null=True)
    searchvector = models.TextField(blank=True)


class newClass(models.Model):
    string = models.CharField(max_length=3000, blank=True)
    resultstring = models.CharField(max_length=3000, blank=True)
    #userID = models.CharField(max_length=512, blank=False)
    #filename = models.CharField(max_length=255, blank=False)
    #reqTestedOn = models.CharField(max_length=512, blank=False)
    #querystring = models.TextField(blank=False)
    #queryArraySize = models.CharField(max_length=512, blank=False)
    #queryArray = ArrayField(models.CharField(max_length=255, blank=True)) # this is a dynamically created array that will store all the teachers lesson plan 'body' content
    #search_vector = SearchVectorField(null=True)
    #searchresults = models.CharField(max_length=512, blank=False)

    # see here for information on ArrayField: https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#arrayfield



















"""from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
#from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/documents/user_<id>/<filename>
    return "documents/%s/%s" %(instance.user.id, filename)

def validate_file_extension(filename):
  import os
  ext = os.path.splitext(filename.name)[1]
  valid_extensions = ['.pdf','.doc','.docx']
  if not ext in valid_extensions:
    raise ValidationError(u'File {0} not supported!'.format(filename))

class Document(models.Model):
    document = models.FileField(upload_to=user_directory_path, null=True, blank=False, validators=[validate_file_extension] )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)"""



