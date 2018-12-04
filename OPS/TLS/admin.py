from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#from .models import UploadData
#admin.site.register(UploadData)


#from .models import PSQLUpload
#admin.site.register(PSQLUpload)

from .models import submissionsModel
class SubmissionsModelAdmin(admin.ModelAdmin):
    model = submissionsModel
    list_display = ('get_userID', 'get_user', 'get_uploadNum', 'get_comment')
admin.site.register(submissionsModel, SubmissionsModelAdmin)    
# Register your models here.
