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
from .models import UploadData
from django.utils.datastructures import MultiValueDictKeyError



     
# Attachment.objects.create(file=each, message=instance)
def Form(request):
        if request.method == 'POST':
                
                # get the files and check for extension errors
                files = request.FILES.getlist("files")
                for file in files:
                        filename = str(file)
                        ext = os.path.splitext(filename)[1]
                        valid_extensions = ['.pdf','.doc','.docx']
                        if not ext in valid_extensions: #check by file extension
                                return HttpResponse('ERROR: File "' + str(filename)+ '" could not be uploaded and caused the other files not to be uploaded as well. Select files that end in docx, pdf, or doc. Return to uploads <a href="/UploadLessonPlan/">here</a>')

                # get the grade level from the form       
                grdLVL = request.POST.get('gradeLevel', '9001') #what it is looking for, default
                requirement = request.POST.get('req', '9001')

                # check for form error
                requirementchk = os.path.splitext(requirement)[0] 
                if grdLVL != requirementchk:
                        return HttpResponse('ERROR: Grade and requirement discrepancy. "' + str(grdLVL) + '" and "' + str(requirementchk) + '" do not match. This caused the files not to be uploaded. Select matching grade and requirements. Return to uploads <a href="/UploadLessonPlan/">here</a>')
      
                if grdLVL == '9001' or requirement == '9001':
                        return HttpResponse('CRITICAL SYSTEM ERROR: Either grade or requirement\'s power levels are over 9000. This caused the files not to be uploaded. Report this error to a system admin. Return to uploads <a href="/UploadLessonPlan/">here</a>')

                
                #get info from auth and update count
                userguy = get_current_user()
                userid = userguy.id
                userguy.incUploads()
                userupload = userguy.getUploads()
                userguy.save()

                # set partial directory and then make the file path if it does not exist
                directory = settings.MEDIA_ROOT + '/documents/' + str(userid) + '/' + str(userupload) + '/'
                if not os.path.exists(directory):
                        os.makedirs(directory)

                # get the count of files, count isnt used - will fix later
                countem = 0 # get count of files uploaded
                for count, x in enumerate(request.FILES.getlist("files")):
                        def process_file(f):
                                with open(directory + str(countem) + '_' + str(f), 'wb+') as destination:     
                                        for chunk in f.chunks():
                                                destination.write(chunk)
                        countem += 1
                        process_file(x) # call the process above

                
                # try to set the UploadData model
                try:
                        userData = UploadData.objects.get(userID=str(userid))
                        userData.grade=grdLVL
                        userData.req = requirement
                        userData.uploadNum = userupload 
                        userData.uploadPath = directory 
                        userData.numberOfFiles = countem
                        userData.save() 
                        #UploadData.objects.filter(
                           #     user__icontains='zach'
                        #)#.filter(
                        #        userID_icontains='27'
                        #)
                except: # if it did not get anything later it will make one now
                        UploadData.objects.create(grade=grdLVL, req = requirement, uploadNum = userupload, user = userguy, userID = userid, uploadPath = directory, numberOfFiles = countem )           

                """if userData.userID != userid:
                        UploadData.objects.create(grade=grdLVL, req = requirement, uploadNum = userupload, user = userguy, userID = userid, uploadPath = directory, numberOfFiles = countem )           
                else:
                        userData.grade=grdLVL
                        userData.req = requirement
                        userData.uploadNum = userupload 
                        userData.uploadPath = directory 
                        userData.numberOfFiles = countem
                        userData.save() """ 
                return HttpResponseRedirect('/UploadResults/') # redirect for success!
        else:
                context = {}
                return render(request, 'home17.html', context) # base view








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

