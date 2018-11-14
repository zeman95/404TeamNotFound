from django import forms
from multiupload.fields import MultiFileField

from django.contrib.auth.models import User



from .models import Message, Attachment
from crum import get_current_user
from django.db.models import F
from users.models import CustomUser
#from .models import specialInc


#def updateUploads(self):
    #currUser = get_current_user()
    #currUser.incUploads()
    #currUser.save()


class UploadForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=30, max_file_size=1024*1024*5)




class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['author_name', 'author_email', 'content']  # not attachments!

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Attachment.objects.create(file=each, message=instance)

        return instance




"""
class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['description'] #['Grade_Level', 'Section_Choice']  # not attachments!
        #GRADE_CHOICES = (
        #    ('6', '6th Grade'),
        #    ('7', '7th Grade'), #First one is the value of select option and second is the displayed value in option
        #    ('8', '8th Grade'),
        #    )
        #widgets = {
        #    'grade': forms.Select(choices=GRADE_CHOICES,attrs={'class': 'form-control'}),
        #}

    files = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Attachment.objects.create(file=each, message=instance)

        return instance"""
        






"""
class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['grade','sections']  # not attachments!

    files = MultiFileField(min_num=1, max_num=30, max_file_size=1024*1024*5)
    #updateUploads

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Attachment.objects.create(file=each, message=instance)#, filenum = filecount, selectnum = inccounter)
        
        return instance"""


        









"""

from django import forms
from multiupload.fields import MultiFileField

from django.contrib.auth.models import User



from .models import Message, Attachment
from crum import get_current_user
from django.db.models import F
from users.models import CustomUser
#from .models import specialInc


#def updateUploads(self):
    #currUser = get_current_user()
    #currUser.incUploads()
    #currUser.save()


class UploadForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=30, max_file_size=1024*1024*5)



class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content',
                'author_name', 'author_email']  # not attachments!

    files = MultiFileField(min_num=1, max_num=30, max_file_size=1024*1024*5)
    #updateUploads

    def save(self, commit=True):
        inccounter = 0
        instance = super(ContactForm, self).save(commit)
        for each in self.cleaned_data['files']:
            if inccounter == 0:
                datuser = CustomUser.objects.get(id='27') 
                datuser.uploads = F('uploads') + 1
                datuser.save()
                inccounter += 1
            Attachment.objects.create(file=each, message=instance, )
        return instance









"""