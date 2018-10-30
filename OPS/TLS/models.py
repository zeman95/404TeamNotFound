from django.db import models

class Document(models.Model):
    #document = models.FileField(upload_to='documents/%Y/%m/%d/'', null=True, blank=False )
    document = models.FileField(upload_to='documents/%Y/%m/%d/', null=True, blank=False )
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
