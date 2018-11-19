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
from pathlib import Path
import re

from django.contrib.postgres.search import SearchVectorField


def Form(request):
        if request.method == 'POST':
                allfilenames = ''
                countz = 0
                # get the files and check for extension errors
                files = request.FILES.getlist("files")
                for file in files:
                        countz += 1
                        filename = str(file)
                        allfilenames = allfilenames + str(countz) + '_' + str(filename) + '#'
                        ext = os.path.splitext(filename)[1]
                        valid_extensions = ['.txt',]
                        if not ext in valid_extensions: #check by file extension
                                return HttpResponse('ERROR: File "' + str(filename)+ '" could not be uploaded and caused the other files not to be uploaded as well. Select files that end in: ' + str(valid_extensions) + '. Return to uploads <a href="/UploadLessonPlans/">here</a>')

                # get the grade level from the form       
                grdLVL = request.POST.get('gradeLevel', '9001') #what it is looking for, default
                requirement = request.POST.get('req', '9001')

                # check for form error
                requirementchk = os.path.splitext(requirement)[0] 
                if grdLVL != requirementchk:
                        return HttpResponse('ERROR: Grade and requirement discrepancy. "' + str(grdLVL) + '" and "' + str(requirementchk) + '" do not match. This caused the files not to be uploaded. Select matching grade and requirements. Return to uploads <a href="/UploadLessonPlans/">here</a>')
      
                if grdLVL == '9001' or requirement == '9001':
                        return HttpResponse('CRITICAL SYSTEM ERROR: Either grade or requirement\'s power levels are over 9000. This caused the files not to be uploaded. Report this error to a system admin. Return to uploads <a href="/UploadLessonPlans/">here</a>')

                
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
                        userData.filenames = allfilenames
                        userData.save() 
                        #UploadData.objects.filter(
                           #     user__icontains='zach'
                        #)#.filter(
                        #        userID_icontains='27'
                        #)
                except: # if it did not get anything later it will make one now
                        UploadData.objects.create(grade=grdLVL, req = requirement, uploadNum = userupload, user = userguy, userID = userid, uploadPath = directory, numberOfFiles = countem, filenames = allfilenames )           
                return HttpResponseRedirect('/UploadResults/') # redirect for success!
        else:
                context = {}
                return render(request, 'home17.html', context) # base view





def cleansing(changeme):
        changeme = str(changeme)
        changeme.replace('b\'\\xef\\xbb\\xbf', '.') 
        return changeme


def home11(request):
        debug = True
        
        # get current logged in user
        userguy = get_current_user()
        userid = userguy.id
                
        # get the users upload data
        userData = UploadData.objects.get(userID=str(userid))
        
        # get the file names in an array
        demFiles = userData.filenames
        demFiles = demFiles.split('#')
        datPath = userData.uploadPath
                
        #if debug: return HttpResponse(str(demFiles[0]))
        
        # open the file, must be a txt file currently
        filecounter = 0
        contents = ''
        while filecounter < int(userData.numberOfFiles):
                # get the file path and name, append then for easy reuse and save contents for processing
                fileselector = str(datPath) + str(demFiles[filecounter])
                f = demFiles[filecounter]
                line = -1
                
                # this code only works with txt format
                with open(fileselector, 'r') as f:
                        contents = f.read()
                
                # This is where files are processed and broken down 
                data = contents.split('\n') # get a copy
                """datalength = len(data)
                if datalength > 2:
                        pass # do nothing
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. Please fix formatting.' )
                datalength = len(data[0])"""

                line += 1
                GRADE = data[line].replace('GRADE: ', '') # get grade  ##########Var
                """if len(GRADE) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. GRADE line is incorrect. Please fix formatting.' )

                datalength = len(data[1]) + len(data[2])"""
                line += 1
                NAME = data[line].replace('FIRSTNAME: ', '') + ' '+ data[line+1].replace('LASTNAME: ', '') # get name  ##########Var
                """if len(NAME) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. FIRSTNAME or LASTNAME line is incorrect. Please fix formatting.' )

                # get information on the page, the current page, and how many there will be, this may be a check for the number of files uploaded
                datalength = len(data[3])"""
                line += 2
                LESSONNUM = data[line].replace('LESSON: ', '') # get the lesson number 
                """if len(LESSONNUM) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. LESSONNUM line is incorrect. Please fix formatting.' )       
                """
                PAGEINFO = LESSONNUM.split('/')
                CURRPAGE = PAGEINFO[0] ##########Var
                MAXPAGE = PAGEINFO[1] ##########Var

                #datalength = len(data[4])
                line += 1
                STANDARD = data[line].replace('STANDARD: ', '') 
                """if len(STANDARD) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. STANDARD line is incorrect. Please fix formatting.' )       
                
                
                datalength = len(data[5])"""
                line += 1
                GOAL= data[line].replace('LEARNING_GOAL: ', '') 
                """if len(GOAL) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. LEARNING_GOAL line is incorrect. Please fix formatting.' )       
                
                datalength = len(data[6])"""
                line += 1
                PHENOMENA= data[line].replace('PHENOMENA: ', '') 
                """if len(PHENOMENA) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. PHENOMENA line is incorrect. Please fix formatting.' )       
                """

                line += 1
                POINTS = data[line].replace('NUMBER_OF_POINTS: ', '')

                endline = line + int(POINTS)
                lessonContent = []     ####### all the lesson plans the teachers wrote are stored here
                while line < endline:
                        line += 1
                        lessonContent.append(data[line])

                line += 1
                SUMMARY = data[line].replace('CLOSING_SUMMARY: ', '')
        


                #######################################################################################
                # now there needs to be a model added to the postgres database to be searched
                #######################################################################################















                #######################################################################################
                # at this point the page has been digested now we need to go and sort out the things?
                #######################################################################################

                # now go and create arrays for each (of the three categories)
                sciEng = []
                disCore = []
                crosscutting = []

                # sort through 'lessonContent' and put each into corresponding list
                """count = 0
                output= ''
                while count < int(POINTS):
                        compareme=str(lessonContent[count])
                        #out = ''
                        #out = re.search('Modeled', compareme)
                        addition = str(count) + ': ' + str(out) + '\n'
                        output = output + addition
                        count += 1"""























                #always last
                filecounter += 1 # go to the next file, or start whichever it is on


                

                
        #if debug: return HttpResponse(str(output))
                
                
                
                
                
                
                
                
                
                
                
        #f = open(str(demFiles[filecounter])),'r') # open the file
        #f.write('hello world')
        #f.close()






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

