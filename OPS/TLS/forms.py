from django import forms
from multiupload.fields import MultiFileField

from django.contrib.auth.models import User



from .models import Message, Attachment


class UploadForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)



class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['description']  # not attachments!

    files = MultiFileField(min_num=1, max_num=5, max_file_size=1024*1024*5)

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit)
        for each in self.cleaned_data['files']:
            Attachment.objects.create(file=each, message=instance)

        return instance









"""from django import forms

from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields= [
            "description",
            "document",
        ]
        widgets={"document":forms.FileInput(attrs={'multiple':True})} # new    """

           