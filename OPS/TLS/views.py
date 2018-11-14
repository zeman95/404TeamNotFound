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
from django.views.generic.edit import FormView, CreateView
from crum import get_current_user
from django.db.models import F
from django.contrib.auth.models import User
from users.models import CustomUser 
from django.contrib.auth import get_user_model

from .forms import ContactForm
from .models import Message
from .forms import UploadForm
from .models import Attachment

import os
from django.conf import settings
     

def Form(request):
        if request.method == 'POST':
                user = get_current_user()
                userid = user.id
                user.incUploads()
                userupload = user.getUploads()
                user.save()

                directory = settings.MEDIA_ROOT + '/documents/' + str(userid) + '/' + str(userupload) + '/'
                if not os.path.exists(directory):
                        os.makedirs(directory)

                for count, x in enumerate(request.FILES.getlist("files")):
                        def process_file(f):
                                with open(directory + str(count) + '.txt', 'wb+') as destination:     
                                        for chunk in f.chunks():
                                                destination.write(chunk)
                        process_file(x) # call the process above
                
                
                
                return HttpResponseRedirect('/UploadResults/')
        else:
                context = {}
                return render(request, 'home17.html', context)








def home11(request):
        context = {}
        return render(request, 'home11.html', context)


class UploadView(FormView):
    template_name = 'home10.html'
    form_class = UploadForm
    success_url = '/UploadResults/'

    def form_valid(self, form):
        for each in form.cleaned_data['attachments']:
            Attachment.objects.create(file=each)
        return super(UploadView, self).form_valid(form)




class ContactView(CreateView):
        #datuser = CustomUser.objects.get(id='27') 
        #datuser.uploads += 1
        #datuser.uploads = F('uploads') + 1
        #datuser.save()
        model = Message
        form_class = ContactForm
        template_name = 'home10.html'
        success_url = '/UploadResults/'
        

        """def form_valid(self, form):
                #datuser = CustomUser.objects.get(id='27') 
                #count = datuser.uploads
                #datuser.uploads = count + 1
                #datuser.uploads = F('uploads') + 1
                #datuser.save()  
                return super(ContactView, self).form_valid(form)"""


   

"""def home10(FormView):
              
        context = {
                        "form": form,
                }
        return render(request, 'home10.html', context)"""

