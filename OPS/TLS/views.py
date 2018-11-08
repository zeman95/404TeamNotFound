"""from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from os import path
import sys
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.shortcuts import HttpResponseRedirect
from .forms import DocumentForm
from django.contrib.auth.models import User



def home10(request):        
        if request.method == 'POST':
                form = DocumentForm(request.POST, request.FILES) # form = DocumentForm(request.POST, request.FILES) 
                if form.is_valid():
                        instance = form.save(commit=False)
                        instance.user = request.user # this was not here orginally
                        form.save()
                        return HttpResponseRedirect('/UploadResults/')
        else:
                form = DocumentForm()
        
        context = {
                        "form": form,
                }
        return render(request, 'home10.html', context)
        

def home11(request):
        context = {}
        return render(request, 'home11.html', context)"""


from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.views import View
from os import path
import sys
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.shortcuts import HttpResponseRedirect

from django.contrib.auth.models import User

from .forms import UploadForm
from .models import Attachment

from django.views.generic.edit import FormView, CreateView

class UploadView(FormView):
    template_name = 'home10.html'
    form_class = UploadForm
    success_url = '/UploadResults/'

    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            Attachment.objects.create(file=each)
        return super(UploadView, self).form_valid(form)

from .forms import ContactForm
from .models import Message


class ContactView(CreateView):
    model = Message
    form_class = ContactForm
    template_name = 'home10.html'
    success_url = '/UploadResults/'


        

def home11(request):
        context = {}
        return render(request, 'home11.html', context)

"""def home10(FormView):
              
        context = {
                        "form": form,
                }
        return render(request, 'home10.html', context)"""

