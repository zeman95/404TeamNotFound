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
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.fields import ArrayField
from .models import PSQLUpload
from .models import newClass
import nltk, re, pprint
from nltk import word_tokenize
from  nltk.text import ConcordanceIndex


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
                except: # if it did not get anything later it will make one now
                        UploadData.objects.create(grade=grdLVL, req = requirement, uploadNum = userupload, user = userguy, userID = userid, uploadPath = directory, numberOfFiles = countem, filenames = allfilenames )           
                return HttpResponseRedirect('/UploadResults/') # redirect for success!
                
        else:
                context = {}
                return render(request, 'home17.html', context) # base view

# this code is supplied from nltk website: https://www.nltk.org/book/ch03.html
# this is not my own code, but the library supplied by nltk written out from stem commands
def stem(word):
     for suffix in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']:
         if word.endswith(suffix):
             return word[:-len(suffix)]
     return word

# code is supplied/based on code from https://simply-python.com/2014/03/14/saving-output-of-nltk-text-concordance/
# give credit where credit is due
# this simply returns the results from an nltk search, the results contain text to either side margin
"""def getLocalResultsFromSearch(searchforthis, searchinthis):
        left_margin = 10 
        right_margin = 10

        ## Create list of tokens using nltk function
        tokens = nltk.word_tokenize(searchinthis)
        
        ## Create the text of tokens
        text = nltk.Text(tokens)
        
        ## Collect all the index or offset position of the target word
        c = nltk.ConcordanceIndex(text.tokens, key = lambda s: s.lower())
        
        ## Collect the range of the words that is within the target word by using text.tokens[start;end].
        ## The map function is use so that when the offset position - the target range < 0, it will be default to zero
        concordance_txt = ([text.tokens[map(lambda x: x-5 if (x-left_margin)>0 else 0,[offset])[0]:offset+right_margin]
                                for offset in c.offsets(searchforthis)])
                                
        ## join the sentences for each of the target phrase and return it
        return [''.join([x+' ' for x in con_sub]) for con_sub in concordance_txt]"""


# this is a rewrite of the concordance library to output to a variable rather than standard out
# code is found from: https://stackoverflow.com/questions/47649987/how-to-save-nltk-concordance-results-in-a-list
# code is derrived from nltk site : http://www.nltk.org/_modules/nltk/text.html#ConcordanceIndex.print_concordance
def concordance(ci, word, width=75, lines=25):
    half_width = (width - len(word) - 2) // 2
    context = width // 4 # approx number of words of context

    results = []
    offsets = ci.offsets(word)
    if offsets:
        lines = min(lines, len(offsets))
        for i in offsets:
            if lines <= 0:
                break
            left = (' ' * half_width +
                    ' '.join(ci._tokens[i-context:i]))
            right = ' '.join(ci._tokens[i+1:i+context])
            left = left[-half_width:]
            right = right[:half_width]
            results.append('%s %s %s' % (left, ci._tokens[i], right))
            lines -= 1

    return results



def home11(request):
        # get current logged in user
        userguy = get_current_user()
        userid = userguy.id
        
        # get the users upload data
        try:
                userData = UploadData.objects.get(userID=str(userid))
                userfileuploads = userData.uploadNum
                chosenreq = userData.req
        except:
                return HttpResponse('Data from last page did not upload correctly. Please go back and try again.')
        
        # get the file names in an array
        demFiles = userData.filenames
        demFiles = demFiles.split('#')
        datPath = userData.uploadPath
                
        #if debug: return HttpResponse(str(demFiles[0]))
        
        # open the file, must be a txt file currently
        filecounter = 0
        contents = ''
        sciEng = []
        disCore = []
        crosscutting = []
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
                GRADE = GRADE.lower()
                """if len(GRADE) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. GRADE line is incorrect. Please fix formatting.' )

                datalength = len(data[1]) + len(data[2])"""
                line += 1
                NAME = data[line].replace('FIRSTNAME: ', '') + ' '+ data[line+1].replace('LASTNAME: ', '') # get name  ##########Var
                NAME = NAME.lower()
                """if len(NAME) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. FIRSTNAME or LASTNAME line is incorrect. Please fix formatting.' )

                # get information on the page, the current page, and how many there will be, this may be a check for the number of files uploaded
                datalength = len(data[3])"""
                line += 2
                LESSONNUM = data[line].replace('LESSON: ', '') # get the lesson number
                LESSONNUM = LESSONNUM.lower() 
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
                STANDARD = STANDARD.lower() 
                """if len(STANDARD) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. STANDARD line is incorrect. Please fix formatting.' )       
                
                
                datalength = len(data[5])"""
                line += 1
                GOAL= data[line].replace('LEARNING_GOAL: ', '')
                GOAL = GOAL.lower() 
                """if len(GOAL) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. LEARNING_GOAL line is incorrect. Please fix formatting.' )       
                
                datalength = len(data[6])"""
                line += 1
                PHENOMENA= data[line].replace('PHENOMENA: ', '') 
                PHENOMENA = PHENOMENA.lower()
                """if len(PHENOMENA) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. PHENOMENA line is incorrect. Please fix formatting.' )       
                """

                line += 1
                POINTS = data[line].replace('NUMBER_OF_POINTS: ', '')

                endline = line + int(POINTS)
                lessonContent = []     ####### all the lesson plans the teachers wrote are stored here
                currentline = ''
                unalteredContent = []
                while line < endline:
                        line += 1
                        unalteredContent.append(data[line])

                        currentline = data[line]
                        currentline = currentline.lower()
                        currentline = currentline.replace('(', '')
                        currentline = currentline.replace(')', '')
                        currentline = currentline.replace('\'', '')
                        currentline = str(demFiles[filecounter]) + ': ' + currentline

                        lessonContent.append(currentline)    #(data[line])

                line += 1
                SUMMARY = data[line].replace('CLOSING_SUMMARY: ', '')
                SUMMARY = SUMMARY.lower()
        


                #######################################################################################
                # now there needs to be a model added to the postgres database to be searched
                #######################################################################################
                # incase somebody redirects back to the same page and doesnt upload a duplicate psqlupload model
                try:
                        psqlModel = PSQLUpload.objects.get(userID=str(userid), uploadNumber = userfileuploads)
                except: # the [:] means in python to iterate over and all the content from the array, so each can be accessed seperately
                        PSQLUpload.objects.create(userID = str(userid), 
                                                filename = str(demFiles[filecounter]), 
                                                uploadNumber = userfileuploads,
                                                reqTestedOn = str(STANDARD), 
                                                queryArraySize = str(POINTS), 
                                                queryArray = lessonContent[:],
                                                querysearch = 'none', 
                                                searchvector = 'none')  
                        psqlModel = PSQLUpload.objects.get(userID=str(userid), uploadNumber = userfileuploads)
                
                
                
                #return HttpResponse(str(psqlModel.queryArray[3]))
               








                #######################################################################################
                # at this point the page has been digested now we need to go and sort out the things?
                #######################################################################################

                # now go and use arrays for each (of the three categories created outside the loop to they dont get overwritten)
                # by handling the lesson content loop
                count = 0

                while count < int(POINTS):
                        # this is done using nltk which works on local variables so it should go much faster
                        # what isgoing on is for this loop one of the sentences is being selected and stemmed
                        # meaning all ending are being removed so when something is being searched we are 
                        # removing all ending so that it will look the same since everything is already lowercase
                        # removing endings should ensure a match if there is one
                        selected = lessonContent[count] # get selected line of code
                        tokens = word_tokenize(selected) # tokenize it
                        
                        # now we are going to stem all the words
                        internalcounter = 0 
                        while internalcounter < len(tokens):
                                tokens[internalcounter] = stem(tokens[internalcounter]) 
                                internalcounter += 1
                        
                        # now piece back to together the string
                        text = nltk.Text(tokens)


                        # now we are going to choose which path the user selected to check
                        if chosenreq == '6.4':
                                pass
                        elif chosenreq == '6.6':
                                pass
                        elif chosenreq == '6.9':
                                pass
                        elif chosenreq == '6.12':
                                pass
                        elif chosenreq == '6.13':
                                # put the tokens back into text to do a search
                                
                                searchterm = stem('modeled') # stem the searchterm
                        
                                ci = ConcordanceIndex(text.tokens)
                                results = concordance(ci, searchterm)
                                
                                if results == None or results == '' or results == []:
                                        pass
                                else:
                                        sciEng.append(lessonContent[count])
                        elif chosenreq == '7.3':
                                pass
                        elif chosenreq == '7.5':
                                pass
                        elif chosenreq == '7.7':
                                pass
                        elif chosenreq == '7.8':
                                pass
                        elif chosenreq == '7.13':
                                pass
                        elif chosenreq == '7.14':
                                pass
                        elif chosenreq == '8.1':
                                pass
                        elif chosenreq == '8.4':
                                pass
                        elif chosenreq == '8.9':
                                pass
                        elif chosenreq == '8.10':
                                pass
                        elif chosenreq == '8.11':
                                pass
                        elif chosenreq == '8.14':
                                pass
                        else:
                                return HttpResponse('Somehow you stumbled upon a lesson that is not supported yet.')
                        
                        

                        
                                #return HttpResponse(str(results))
                                

                        
                                                        

                        
                        
                        
                        
                        
                        
                        
                        
                       # return HttpResponse(text.similar(str(searchterm)))            #str(tokens))
                        





                        count += 1
                #always last
                filecounter += 1 # go to the next file, or start whichever it is on


                

                
        return HttpResponse(sciEng)
                
                
                
                
                
                
                
                
                
                
                
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

