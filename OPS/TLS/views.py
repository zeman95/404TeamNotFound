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

#from django.contrib.postgres.search import SearchVectorField
#from django.contrib.postgres.search import SearchVector
#from django.contrib.postgres.fields import ArrayField
#from .models import PSQLUpload
from .models import newClass
import nltk, re, pprint
from nltk import word_tokenize
from  nltk.text import ConcordanceIndex
from PyDictionary import PyDictionary
from .models import submissionsModel


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
     for suffix in ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment',]:
         if word.endswith(suffix):
             return word[:-len(suffix)]
     return word



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


def search(searchkeyword, texttosearch):
        searchterm = stem(searchkeyword) # stem the searchterm               
        ci = ConcordanceIndex(texttosearch.tokens)
        results = concordance(ci, searchterm)
        return results

def removeSpecialCases(changeme):
        changeme = changeme.lower() # force to lower

        # now remove all special characters allowed by general ascii
        changeme = changeme.replace('(', '')
        changeme = changeme.replace(')', '')
        changeme = changeme.replace('\'', '')
        changeme = changeme.replace('.', '')
        changeme = changeme.replace(',', '')
        changeme = changeme.replace('?', '')
        changeme = changeme.replace('\"', '')
        changeme = changeme.replace('\\', '')
        changeme = changeme.replace('/', '')
        changeme = changeme.replace(':', '')
        changeme = changeme.replace(';', '')
        changeme = changeme.replace('!', '')
        changeme = changeme.replace('@', '')
        changeme = changeme.replace('#', '')
        changeme = changeme.replace('$', '')
        changeme = changeme.replace('%', '')
        changeme = changeme.replace('^', '')
        changeme = changeme.replace('&', '')
        changeme = changeme.replace('*', '')
        changeme = changeme.replace('-', '')
        changeme = changeme.replace('_', '')
        changeme = changeme.replace('+', '')
        changeme = changeme.replace('=', '')
        changeme = changeme.replace('`', '')
        changeme = changeme.replace('~', '')
        changeme = changeme.replace('|', '')
        changeme = changeme.replace('}', '')
        changeme = changeme.replace('{', '')
        changeme = changeme.replace('[', '')
        changeme = changeme.replace(']', '')
        changeme = changeme.replace('“', '') # this is considered a special case for some reason?
        changeme = changeme.replace('”', '') # this is also considered a special case?
        changeme = changeme.replace('>', '')
        changeme = changeme.replace('<', '')

        # now stem the words
        try:
                allwords = changeme.split(' ')
                x = 0
                while x < len(allwords):
                        allwords[x] = stem(allwords[x])
                        x += 1

                x = 0
                templine = ''
                while x < len(allwords):
                        templine = templine + allwords[x] + ' '
                        x += 1

                changeme = templine
        except:
                return HttpResponse('There was an error parsing in the input from a line. Please make sure there is actually something there to work with.')

        return changeme



def home11(request):
        # create the dictonary
        dictionary=PyDictionary()

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
        sciEngDisplay = []
        disCore = []
        disCoreDisplay = []
        crosscutting = []
        crosscuttingDisplay = []
        algorithm = []
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
                datalength = len(data)
                if datalength > 2:
                        pass # do nothing
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. Please fix formatting.' )
                datalength = len(data[0])

                line += 1
                GRADE = data[line].replace('GRADE: ', '') # get grade  ##########Var
                GRADE = GRADE.lower()
                if len(GRADE) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. GRADE line is incorrect. Please fix formatting.' )

                datalength = len(data[1]) + len(data[2])
                line += 1
                NAME = data[line].replace('FIRSTNAME: ', '') + ' '+ data[line+1].replace('LASTNAME: ', '') # get name  ##########Var
                NAME = NAME.lower()
                if len(NAME) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. FIRSTNAME or LASTNAME line is incorrect. Please fix formatting.' )

                # get information on the page, the current page, and how many there will be, this may be a check for the number of files uploaded
                datalength = len(data[3])
                line += 2
                LESSONNUM = data[line].replace('LESSON: ', '') # get the lesson number
                LESSONNUM = LESSONNUM.lower() 
                if len(LESSONNUM) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. LESSONNUM line is incorrect. Please fix formatting.' )       
                
                PAGEINFO = LESSONNUM.split('/')
                CURRPAGE = PAGEINFO[0] ##########Var
                MAXPAGE = PAGEINFO[1] ##########Var

                datalength = len(data[4])
                line += 1
                STANDARD = data[line].replace('STANDARD: ', '')
                STANDARD = STANDARD.lower() 
                if len(STANDARD) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. STANDARD line is incorrect. Please fix formatting.' )       
                
                
                datalength = len(data[5])
                line += 1
                GOAL= data[line].replace('LEARNING_GOAL: ', '')
                GOAL = GOAL.lower() 
                if len(GOAL) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. LEARNING_GOAL line is incorrect. Please fix formatting.' )       
                
                datalength = len(data[6])
                line += 1
                PHENOMENA= data[line].replace('PHENOMENA: ', '') 
                PHENOMENA = PHENOMENA.lower()
                if len(PHENOMENA) < datalength:
                        pass
                else:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. PHENOMENA line is incorrect. Please fix formatting.' )       
                

                line += 1
                POINTS = data[line].replace('NUMBER_OF_POINTS: ', '')
                try:
                        if int(POINTS) > 0:
                                pass
                        else:
                                return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. POINTS line is incorrect - must be more than 0. Please fix formatting.' )       

                except:
                                return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. POINTS line is incorrect - must be more than 0. Please fix formatting.' )       

                #######################################################################################
                # now the input from the text file needs to be processed
                #######################################################################################
                try:
                        x = 0
                        endline = line + int(POINTS)
                        lessonContent = []     ####### all the lesson plans the teachers wrote are stored here
                        currentline = ''
                        unalteredContent = []
                        templine = ''
                        while line < endline:
                                x = 0
                                line += 1
                                currentline = data[line]
                                
                                currentline = removeSpecialCases(currentline) # removes all special cases, punctuations and suchforth from line
                                currentline = str(demFiles[filecounter]) + ': ' + currentline # append the filename on
                                lessonContent.append(currentline)    # this is the modified array the program will be using, not suitable for output
                                
                                currentline = str(demFiles[filecounter]) + ': ' + data[line]
                                unalteredContent.append(currentline) # this is the unaltered array for output to screen
                except:
                        return HttpResponse('File named: ' + str(demFiles[filecounter]) + ' was formatted incorrectly. Lesson content is incorrect - make sure number of points matches the number of lesson plan bullets. Please fix formatting.' )       


                        

                line += 1
                SUMMARY = data[line].replace('CLOSING_SUMMARY: ', '')
                SUMMARY = SUMMARY.lower()
        


                """#######################################################################################
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
                        psqlModel = PSQLUpload.objects.get(userID=str(userid), uploadNumber = userfileuploads)"""

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
                        
                        # now piece back to together the string from the altered string
                        text = nltk.Text(tokens)

                        # create an array the size of the lesson plans
                        # we are going to allow each to map to as many as possible
                        mapped = []
                        x = 0
                        while x < int(POINTS):
                                mapped.append(False)
                                x += 1

                        # now we are going to choose which path the user selected to check
                        # each of these has to be based upon the lesson content requirements themselves, each MUST
                        # be custom
                        if chosenreq == '6.4':
                                pass
                        elif chosenreq == '6.6':
                                pass
                        elif chosenreq == '6.9':
                                pass
                        elif chosenreq == '6.12':
                                pass
                        elif chosenreq == '6.13':
                                #######################################################################################
                                # Check the science and engineering column
                                #######################################################################################
                                chosenstring = ''
                                searchthis = []
                                searchthis = ['modeled', 'drawing', 'diagram', 'create', 'gameboard', 'display', 'replica', 'representation', 'duplicate',] # words here will be searched for relevance, manually - still need to be stemmed also
                                x = 0
                                while x < len(searchthis):
                                        searchthis[x] = stem(searchthis[x]) # stem it
                                        x += 1
                                
                                for word in searchthis: # iterate through the array of words
                                        try: #try to get synonyms if there is any
                                                synonyms = str(dictionary.synonym(str(word))) # uses pydictonary to get synonyms instead of coding them all of them
                                                
                                                # now stem the synonyms
                                                x = 0
                                                while x < len(synonyms):
                                                        synonyms[x] = stem(synonyms[x]) # stem it
                                                        x += 1
                                                
                                                for syn in synonyms:
                                                        results = search(str(syn), text) # search the term, and then the text you want to search
                                                        if results == None or results == '' or results == []:
                                                                pass # nothing was found
                                                        elif mapped[count] == False: # if it has not been mapped allow it
                                                                chosenstring = unalteredContent[count]
                                                                #chosenstring = chosenstring[:35] + '...'  # trimming code
                                                                sciEngDisplay.append(chosenstring) # this is the unaltered content for display
                                                                sciEng.append(lessonContent[count])
                                                                mapped[count] = True # now its been mapped, keeps things from being mapped twice
                                        except: # if there isnt a synonym for the word, we must continue on
                                                results = search(str(word), text) # search the term, and then the text you want to search
                                                if results == None or results == '' or results == []:
                                                        pass # nothing was found
                                                elif mapped[count] == False: # if it has not been mapped allow it
                                                        chosenstring = unalteredContent[count] # this chooses from the unaltered content array
                                                        #chosenstring = chosenstring[:35] + '...'  # trimming code
                                                        sciEngDisplay.append(chosenstring) # this is the unaltered content for display
                                                        sciEng.append(lessonContent[count])
                                                        mapped[count] = True # now its been mapped, keeps things from being mapped twice
                                # clear the array, since we allow remapping
                                x = 0
                                while x < int(POINTS):
                                        mapped[x] = False
                                        x += 1

                                


                                #######################################################################################
                                # Disciplinary core ideas
                                #######################################################################################
                                chosenstring = ''
                                searchthis = []
                                searchthis = ['processes', 'cycle', 'water', 'transpiration', 
                                'sunlight', 'gravity', 'ocean', 'lake', 'river', 'condensation', 'clouds', 'runoff',
                                'crystalization', 'precipitation', 'land', 'atmosphere', 'evaporation', 'form', 'change'] # words here will be searched for relevance, manually - still need to be stemmed also
                                x = 0
                                while x < len(searchthis):
                                        searchthis[x] = stem(searchthis[x]) # stem it
                                        x += 1
                                
                                for word in searchthis: # iterate through the array of words
                                        try: #try to get synonyms if there is any
                                                synonyms = str(dictionary.synonym(str(word))) # uses pydictonary to get synonyms instead of coding them all of them
                                                
                                                # now stem the synonyms
                                                x = 0
                                                while x < len(synonyms):
                                                        synonyms[x] = stem(synonyms[x]) # stem it
                                                        x += 1
                                                
                                                for syn in synonyms:
                                                        results = search(str(syn), text) # search the term, and then the text you want to search
                                                        if results == None or results == '' or results == []:
                                                                pass # nothing was found
                                                        elif mapped[count] == False: # if it has not been mapped allow it
                                                                chosenstring = unalteredContent[count]
                                                                #chosenstring = chosenstring[:35] + '...'  # trimming code
                                                                disCoreDisplay.append(chosenstring) # this is the unaltered content for display
                                                                disCore.append(lessonContent[count])
                                                                mapped[count] = True # now its been mapped, keeps things from being mapped twice
                                        except: # if there isnt a synonym for the word, we must continue on
                                                results = search(str(word), text) # search the term, and then the text you want to search
                                                if results == None or results == '' or results == []:
                                                        pass # nothing was found
                                                elif mapped[count] == False: # if it has not been mapped allow it
                                                        chosenstring = unalteredContent[count] # this chooses from the unaltered content array
                                                        #chosenstring = chosenstring[:35] + '...'  # trimming code
                                                        disCoreDisplay.append(chosenstring) # this is the unaltered content for display
                                                        disCore.append(lessonContent[count])
                                                        mapped[count] = True # now its been mapped, keeps things from being mapped twice
                                # clear the array, since we allow remapping
                                x = 0
                                while x < int(POINTS):
                                        mapped[x] = False
                                        x += 1

                                
                                #######################################################################################
                                # Cross cutting concepts
                                #######################################################################################
                                chosenstring = ''
                                searchthis = []
                                searchthis = ['energy', 'matter', 'system', 'transfer', 'drives', 'motion', 
                                'cycling', 'cause', 'effect', 'relationships'] # words here will be searched for relevance, manually - still need to be stemmed also
                                x = 0
                                while x < len(searchthis):
                                        searchthis[x] = stem(searchthis[x]) # stem it
                                        x += 1
                                
                                for word in searchthis: # iterate through the array of words
                                        try: #try to get synonyms if there is any
                                                synonyms = str(dictionary.synonym(str(word))) # uses pydictonary to get synonyms instead of coding them all of them
                                                
                                                # now stem the synonyms
                                                x = 0
                                                while x < len(synonyms):
                                                        synonyms[x] = stem(synonyms[x]) # stem it
                                                        x += 1
                                                
                                                for syn in synonyms:
                                                        results = search(str(syn), text) # search the term, and then the text you want to search
                                                        if results == None or results == '' or results == []:
                                                                pass # nothing was found
                                                        elif mapped[count] == False: # if it has not been mapped allow it
                                                                chosenstring = unalteredContent[count]
                                                                #chosenstring = chosenstring[:35] + '...'  # trimming code
                                                                crosscuttingDisplay.append(chosenstring) # this is the unaltered content for display
                                                                crosscutting.append(lessonContent[count])
                                                                mapped[count] = True # now its been mapped, keeps things from being mapped twice
                                        except: # if there isnt a synonym for the word, we must continue on
                                                results = search(str(word), text) # search the term, and then the text you want to search
                                                if results == None or results == '' or results == []:
                                                        pass # nothing was found
                                                elif mapped[count] == False: # if it has not been mapped allow it
                                                        chosenstring = unalteredContent[count] # this chooses from the unaltered content array
                                                        #chosenstring = chosenstring[:35] + '...'  # trimming code
                                                        crosscuttingDisplay.append(chosenstring) # this is the unaltered content for display
                                                        crosscutting.append(lessonContent[count])
                                                        mapped[count] = True # now its been mapped, keeps things from being mapped twice
                                # clear the array, since we allow remapping
                                x = 0
                                while x < int(POINTS):
                                        mapped[x] = False
                                        x += 1
                                
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
                        count += 1
                filecounter += 1 # go to the next file, or start whichever it is on, this is always last in this loop
                # this is the end of the file searching, everything that is needed now is already saved



        #######################################################################################
        # now that everything has been sorted out for three categories on all files, work on rubric
        #######################################################################################
        if chosenreq == '6.4':
                        pass
        elif chosenreq == '6.6':
                pass
        elif chosenreq == '6.9':
                pass
        elif chosenreq == '6.12':
                pass
        elif chosenreq == '6.13':          
                ###################################################################################
                # Part 1"A"
                ##################################################################################
                outputToScreen = ''
                componetsOfModel = []
                # setup boolean array to match criteria
                foundCompOfModel = [0] * 6   #[6] # there is 6 criteria for 
                foundSubCompOfModel = [0] * 11     #[11] # this is the total of criteria keywords
        
                if (len(sciEng) >= 1): # this means that the user inputted somthing about a model, and  main on 6.13.5.A is satisfied
                        # 
                        #       Components of the model. Search the lines in sciEngineering that correspond to the model
                        #
                                
                        sciEngCopy = sciEng # get a copy of scieng for splicing since it has 1 or more

                        searchthis = []
                        searchthis = ['water', 'liquid', 'solid', 'gas', #1 
                                        'sunlight',  #2
                                        'gravity', #3
                                        'atmosphere', #4 
                                        'land', 'landforms', #5 
                                        'plants', 'living'] #6
                        # stem search terms
                        x = 0
                        while x < len(searchthis):
                                searchthis[x] = stem(searchthis[x]) # stem it
                                x += 1   
                                
                        count = 0
                        while count < len(sciEngCopy): # same length as the og
                                # this is done using nltk which works on local variables so it should go much faster
                                # what isgoing on is for this loop one of the sentences is being selected and stemmed
                                # meaning all ending are being removed so when something is being searched we are 
                                # removing all ending so that it will look the same since everything is already lowercase
                                # removing endings should ensure a match if there is one
                                selected = sciEngCopy[count] # get selected line of code
                                tokens = word_tokenize(selected) # tokenize it
                                        
                                # now we are going to stem all the words
                                internalcounter = 0 
                                while internalcounter < len(tokens):
                                        tokens[internalcounter] = stem(tokens[internalcounter]) 
                                        internalcounter += 1
                                        
                                # now piece back to together the string from the altered string
                                text = nltk.Text(tokens)
                                
                                for word in searchthis: # iterate through the array of words
                                        try: #try to get synonyms if there is any
                                                synonyms = str(dictionary.synonym(str(word))) # uses pydictonary to get synonyms instead of coding them all of them
                                                        
                                                # now stem the synonyms
                                                x = 0
                                                while x < len(synonyms):
                                                        synonyms[x] = stem(synonyms[x]) # stem it
                                                        x += 1
                                                        
                                                for syn in synonyms:
                                                        results = search(str(syn), text) # search the term, and then the text you want to search
                                                        if results == None or results == '' or results == []:
                                                                pass # nothing was found
                                                        else: # means that it has been found
                                                                # 1
                                                                if (word == stem('water')):
                                                                        foundSubCompOfModel[0] = 1 # found
                                                                if (word == stem('liquid')):
                                                                        foundSubCompOfModel[1] = 1 # found
                                                                if (word == stem('solid')):
                                                                        foundSubCompOfModel[2] = 1 # found
                                                                if (word == stem('gas')):
                                                                        foundSubCompOfModel[3] = 1 # found
                                                                        #crosscutting.append(sciEng[count])

                                                                # 2
                                                                if (word == stem('sunlight')):
                                                                        foundSubCompOfModel[4] = 1 # found
                                                                        #crosscutting.append(sciEng[count])
                                                                        
                                                                # 3
                                                                if (word == stem('gravity')):
                                                                        foundSubCompOfModel[5] = 1 # found
                                                                        #crosscutting.append(sciEng[count])
                                                                        
                                                                # 4
                                                                if (word == stem('atmosphere')):
                                                                        foundSubCompOfModel[6] = 1 # found
                                                                        #crosscutting.append(sciEng[count])
                                                                        
                                                                # 5
                                                                if (word == stem('land') or word == stem('landforms')):
                                                                        foundSubCompOfModel[7] = 1 # found
                                                                        foundSubCompOfModel[8] = 1 # found
                                                                        #crosscutting.append(sciEng[count])
                                                                # 6
                                                                if (word == stem('plants')):
                                                                        foundSubCompOfModel[9] = 1 # found
                                                                if (word == stem('living') and foundSubCompOfModel[9] == 1):
                                                                        foundSubCompOfModel[10] = 1 # found
                                        except: # if there isnt a synonym for the word, we must continue on
                                                results = search(str(word), text) # search the term, and then the text you want to search
                                                if results == None or results == '' or results == []:
                                                        pass # nothing was found
                                                else: # means that it has been found
                                                        # 1
                                                        if (word == stem('water')):
                                                                foundSubCompOfModel[0] = 1 # found
                                                        if (word == stem('liquid')):
                                                                foundSubCompOfModel[1] = 1 # found
                                                        if (word == stem('solid')):
                                                                foundSubCompOfModel[2] = 1 # found
                                                        if (word == stem('gas')):
                                                                foundSubCompOfModel[3] = 1 # found
                                                                #crosscutting.append(sciEng[count])

                                                        # 2
                                                        if (word == stem('sunlight')):
                                                                foundSubCompOfModel[4] = 1 # found
                                                                #crosscutting.append(sciEng[count])
                                                                        
                                                        # 3
                                                        if (word == stem('gravity')):
                                                                foundSubCompOfModel[5] = 1 # found
                                                                #crosscutting.append(sciEng[count])
                                                                        
                                                        # 4
                                                        if (word == stem('atmosphere')):
                                                                foundSubCompOfModel[6] = 1 # found
                                                                #crosscutting.append(sciEng[count])
                                                                        
                                                        # 5
                                                        if (word == stem('land') or word == stem('landforms')):
                                                                foundSubCompOfModel[7] = 1 # found
                                                                foundSubCompOfModel[8] = 1 # found
                                                                #crosscutting.append(sciEng[count])
                                                        # 6
                                                        if (word == stem('plants')):
                                                                foundSubCompOfModel[9] = 1 # found
                                                        if (word == stem('living') and foundSubCompOfModel[9] == 1):
                                                                foundSubCompOfModel[10] = 1 # found
                                count += 1
                        
                        # set the found items
                        tester = 0 # this will test all the parts of the array
                        
                        partials = 0 # count the number, if more than half is found might as well add it since nobody will ever match all of these
                        maxloop = 4
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[0] = 1
                                outputToScreen = outputToScreen + '1.a.i.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '1.a.i.: Not Found' + '\n'
                                        
                        partials = 0
                        maxloop = 5
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[1] = 1
                                outputToScreen = outputToScreen + '1.a.ii.: Found' + '\n'
                                
                        else:
                                outputToScreen = outputToScreen + '1.a.ii.: Not Found' + '\n'


                        partials = 0
                        maxloop = 6
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[2] = 1
                                outputToScreen = outputToScreen + '1.a.iii.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '1.a.iii.: Not Found' + '\n'


                        partials = 0
                        maxloop = 7
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[3] = 1
                                outputToScreen = outputToScreen + '1.a.iv.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '1.a.iv.: Not Found' + '\n'


                        partials = 0
                        maxloop = 9
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[4] = 1
                                outputToScreen = outputToScreen + '1.a.v.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '1.a.v.: Not Found' + '\n'



                        if foundSubCompOfModel[9] == 1 and foundSubCompOfModel[10] == 1:
                                foundCompOfModel[5] = 1
                                outputToScreen = outputToScreen + '1.a.vi.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '1.a.vi.: Not Found' + '\n'



                        # is it a partial match or non at all?
                        count = 0
                        numfound = 0
                        while count < len(foundCompOfModel):
                                if (foundCompOfModel[count] == 1):
                                        numfound += 1
                                count += 1
                                        
                        if numfound == len(foundCompOfModel):
                                outputToScreen = '6.13.5.A \n' +  '\n1. Components: Complete Match \n' + outputToScreen
                        elif numfound > 0 and numfound < len(foundCompOfModel):
                                outputToScreen = '6.13.5.A \n' +  '\n1. Components: Partial Match \n' + outputToScreen
                        elif numfound == 0:
                                outputToScreen = '6.13.5.A \n' +  '\n1. Components: No Matches Discovered \n' + outputToScreen# no need to output things it didnt find


                        algorithm.append(outputToScreen) # save into array
                        
                        
                        
                        
                        
                        
                        outputToScreen = '' 
                        foundCompOfModel = []
                        foundSubCompOfModel = []
                        ####################################################################################
                        # this is going to be part 2
                        ####################################################################################
                        searchthis = [] # clear array, then make the search terms
                        searchthis = [  'energy', 'transfer', 'sun', 'warms', 'evaporate',                                      # i, 5 tot
                                        'water', 'vapor', 'atmosphere', 'forms', 'clouds', 'condense', 'preciptation', 'falls', # ii, 8 tot 
                                        'gravity', 'downhill', 'flow', 'oceans',                                                # iii, 4 tot
                                        'remain', 'land',                                                                       # iv, 2 tot
                                        'tissues', 'plants', 'organisms', 'decompose',                                          # v, 4 tot
                        ]                                                       
                        foundCompOfModel = [0] * 5
                        foundSubCompOfModel = [0] * len(searchthis)   #(5+8+4+2+4)


                        # stem search terms
                        x = 0
                        while x < len(searchthis):
                                searchthis[x] = stem(searchthis[x]) # stem it
                                x += 1   
                                
                        count = 0
                        sciEngCopy = sciEng
                        while count < len(sciEngCopy): # same length as the og
                                # this is done using nltk which works on local variables so it should go much faster
                                # what isgoing on is for this loop one of the sentences is being selected and stemmed
                                # meaning all ending are being removed so when something is being searched we are 
                                # removing all ending so that it will look the same since everything is already lowercase
                                # removing endings should ensure a match if there is one
                                selected = sciEngCopy[count] # get selected line of code
                                tokens = word_tokenize(selected) # tokenize it
                                        
                                # now we are going to stem all the words
                                internalcounter = 0 
                                while internalcounter < len(tokens):
                                        tokens[internalcounter] = stem(tokens[internalcounter]) 
                                        internalcounter += 1
                                        
                                # now piece back to together the string from the altered string
                                text = nltk.Text(tokens)
                                
                                for word in searchthis: # iterate through the array of words
                                        try: #try to get synonyms if there is any
                                                synonyms = str(dictionary.synonym(str(word))) # uses pydictonary to get synonyms instead of coding them all of them
                                                        
                                                # now stem the synonyms
                                                x = 0
                                                while x < len(synonyms):
                                                        synonyms[x] = stem(synonyms[x]) # stem it
                                                        x += 1
                                                        
                                                for syn in synonyms:
                                                        results = search(str(syn), text) # search the term, and then the text you want to search
                                                        if results == None or results == '' or results == []:
                                                                pass # nothing was found
                                                        else: # means that it has been found
                                                                # 1
                                                                if (word == stem('energy')):
                                                                        foundSubCompOfModel[0] = 1 # found
                                                                if (word == stem('transfer')):
                                                                        foundSubCompOfModel[1] = 1 # found)
                                                                if (word == stem('sun')):
                                                                        foundSubCompOfModel[2] = 1 # found
                                                                if (word == stem('warms')):
                                                                        foundSubCompOfModel[3] = 1 # found)
                                                                if (word == stem('evaporate')):
                                                                        foundSubCompOfModel[4] = 1 # found)


                                                                # 2
                                                                if (word == stem('water')):
                                                                        foundSubCompOfModel[5] = 1 # found
                                                                if (word == stem('vapor')):
                                                                        foundSubCompOfModel[6] = 1 # found)
                                                                if (word == stem('atmosphere')):
                                                                        foundSubCompOfModel[7] = 1 # found
                                                                if (word == stem('forms')):
                                                                        foundSubCompOfModel[8] = 1 # found)
                                                                if (word == stem('clouds')):
                                                                        foundSubCompOfModel[9] = 1 # found)
                                                                if (word == stem('condense')):
                                                                        foundSubCompOfModel[10] = 1 # found)
                                                                if (word == stem('precipitation') or word == stem('falls')):
                                                                        foundSubCompOfModel[11] = 1 # found
                                                                        foundSubCompOfModel[12] = 1 # found)
                                                                
                                                                        
                                                                # 3
                                                                if (word == stem('gravity')):
                                                                        foundSubCompOfModel[13] = 1 # found
                                                                if (word == stem('downhill')):
                                                                        foundSubCompOfModel[14] = 1 # found)
                                                                if (word == stem('flow')):
                                                                        foundSubCompOfModel[15] = 1 # found
                                                                if (word == stem('oceans')):
                                                                        foundSubCompOfModel[16] = 1 # found)
                                                                

                                                                # 4
                                                                if (word == stem('remain')):
                                                                        foundSubCompOfModel[17] = 1 # found
                                                                if (word == stem('land')):
                                                                        foundSubCompOfModel[18] = 1 # found)
                                                                        
                                                                # 5
                                                                if (word == stem('tissues')):
                                                                        foundSubCompOfModel[19] = 1 # found
                                                                if (word == stem('plants')):
                                                                        foundSubCompOfModel[20] = 1 # found)
                                                                if (word == stem('organisms')):
                                                                        foundSubCompOfModel[21] = 1 # found)
                                                                if (word == stem('decompose')):
                                                                        foundSubCompOfModel[22] = 1 # found)
                                                            
                                        except: # if there isnt a synonym for the word, we must continue on
                                                results = search(str(word), text) # search the term, and then the text you want to search
                                                if results == None or results == '' or results == []:
                                                        pass # nothing was found
                                                else: # means that it has been found
                                                        # 1
                                                        if (word == stem('energy')):
                                                                foundSubCompOfModel[0] = 1 # found
                                                        if (word == stem('transfer')):
                                                                foundSubCompOfModel[1] = 1 # found)
                                                        if (word == stem('sun')):
                                                                foundSubCompOfModel[2] = 1 # found
                                                        if (word == stem('warms')):
                                                                foundSubCompOfModel[3] = 1 # found)
                                                        if (word == stem('evaporate')):
                                                                foundSubCompOfModel[4] = 1 # found)


                                                        # 2
                                                        if (word == stem('water')):
                                                                foundSubCompOfModel[5] = 1 # found
                                                        if (word == stem('vapor')):
                                                                foundSubCompOfModel[6] = 1 # found)
                                                        if (word == stem('atmosphere')):
                                                                foundSubCompOfModel[7] = 1 # found
                                                        if (word == stem('forms')):
                                                                foundSubCompOfModel[8] = 1 # found)
                                                        if (word == stem('clouds')):
                                                                foundSubCompOfModel[9] = 1 # found)
                                                        if (word == stem('condense')):
                                                                foundSubCompOfModel[10] = 1 # found)
                                                        if (word == stem('precipitation') or word == stem('falls')):
                                                                foundSubCompOfModel[11] = 1 # found
                                                                foundSubCompOfModel[12] = 1 # found)
                                                        
                                                                
                                                        # 3
                                                        if (word == stem('gravity')):
                                                                foundSubCompOfModel[13] = 1 # found
                                                        if (word == stem('downhill')):
                                                                foundSubCompOfModel[14] = 1 # found)
                                                        if (word == stem('flow')):
                                                                foundSubCompOfModel[15] = 1 # found
                                                        if (word == stem('oceans')):
                                                                foundSubCompOfModel[16] = 1 # found)
                                                        

                                                        # 4
                                                        if (word == stem('remain')):
                                                                foundSubCompOfModel[17] = 1 # found
                                                        if (word == stem('land')):
                                                                foundSubCompOfModel[18] = 1 # found)
                                                                
                                                        # 5
                                                        if (word == stem('tissues')):
                                                                foundSubCompOfModel[19] = 1 # found
                                                        if (word == stem('plants')):
                                                                foundSubCompOfModel[20] = 1 # found)
                                                        if (word == stem('organisms')):
                                                                foundSubCompOfModel[21] = 1 # found)
                                                        if (word == stem('decompose')):
                                                                foundSubCompOfModel[22] = 1 # found)
                                                       
                                count += 1
                        # set the found items
                        tester = 0 # this will test all the parts of the array
                        
                        partials = 0 # count the number, if more than half is found might as well add it since nobody will ever match all of these
                        maxloop = 5
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[0] = 1
                                outputToScreen = outputToScreen + '2.a.i.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '2.a.i.: Not Found' + '\n'
                                        
                        partials = 0
                        maxloop = 13
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[1] = 1
                                outputToScreen = outputToScreen + '2.a.ii.: Found' + '\n'
                                
                        else:
                                outputToScreen = outputToScreen + '2.a.ii.: Not Found' + '\n'


                        partials = 0
                        maxloop = 17
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[2] = 1
                                outputToScreen = outputToScreen + '2.a.iii.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '2.a.iii.: Not Found' + '\n'


                        partials = 0
                        maxloop = 19
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[3] = 1
                                outputToScreen = outputToScreen + '2.a.iv.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '2.a.iv.: Not Found' + '\n'


                        partials = 0
                        maxloop = 23
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[4] = 1
                                outputToScreen = outputToScreen + '2.a.v.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '2.a.v.: Not Found' + '\n'




                        # is it a partial match or non at all?
                        count = 0
                        numfound = 0
                        while count < len(foundCompOfModel):
                                if (foundCompOfModel[count] == 1):
                                        numfound += 1
                                count += 1
                                        
                        if numfound == len(foundCompOfModel):
                                outputToScreen = '6.13.5.A \n' +  '2. Relationships: Complete Match \n' + outputToScreen
                        elif numfound > 0 and numfound < len(foundCompOfModel):
                                outputToScreen = '6.13.5.A \n' +  '2. Relationships: Partial Match \n' + outputToScreen
                        elif numfound == 0:
                                outputToScreen = '6.13.5.A \n' +  '2. Relationships: No Matches Discovered \n' + outputToScreen # no need to output things it didnt find

                        algorithm.append(outputToScreen) # save into array






                        outputToScreen = '' 
                        foundCompOfModel = []
                        foundSubCompOfModel = []
                        ####################################################################################
                        # this is going to be part 3
                        ####################################################################################
                        searchthis = [] # clear array, then make the search terms
                        searchthis = [  'energy', 'sun', 'movement', 'transpiration', 'evaporate',                                      # ai,
                                        'water', 'vapor', 'atmosphere', 'condense', 'form', 'crystallize ', 'snow', 'ice', 'gravity', # aii, 
                                        'gravity', 'surface', 'water', 'rivers', 'flow', 'ocean',                                                # aiii1, 
                                        'evaporate', 'atmosphere',  #aiii2
                                        'plants', 'transpiration', 'decomposition',                                                                       # aiii3, 
                                        'animals', 'respiration', 'decomposition',                                                                       # aiii4, 
                                        'freeze', 'crystallize', 'frozen', 'form', 'glaciers', 'ice',                                                                       # aiii5, 
                                        'water', 'below', 'ground', 'aquifers',                                                                       # aiii6, 
                                        'evaporation', 'transpiration', 'condensation', 'crystallization', 'precipitation',                                                                       # b,
                                        'phases', 'locations', 'surface', 'atmosphere',                                          # c, 
                        ]                                                       
                        foundCompOfModel = [0] * 5
                        foundSubCompOfModel = [0] * len(searchthis)   #(5+8+4+2+4)


                        # stem search terms
                        x = 0
                        while x < len(searchthis):
                                searchthis[x] = stem(searchthis[x]) # stem it
                                x += 1   
                                
                        count = 0
                        sciEngCopy = sciEng
                        while count < len(sciEngCopy): # same length as the og
                                # this is done using nltk which works on local variables so it should go much faster
                                # what isgoing on is for this loop one of the sentences is being selected and stemmed
                                # meaning all ending are being removed so when something is being searched we are 
                                # removing all ending so that it will look the same since everything is already lowercase
                                # removing endings should ensure a match if there is one
                                selected = sciEngCopy[count] # get selected line of code
                                tokens = word_tokenize(selected) # tokenize it
                                        
                                # now we are going to stem all the words
                                internalcounter = 0 
                                while internalcounter < len(tokens):
                                        tokens[internalcounter] = stem(tokens[internalcounter]) 
                                        internalcounter += 1
                                        
                                # now piece back to together the string from the altered string
                                text = nltk.Text(tokens)
                                
                                for word in searchthis: # iterate through the array of words
                                        try: #try to get synonyms if there is any
                                                synonyms = str(dictionary.synonym(str(word))) # uses pydictonary to get synonyms instead of coding them all of them
                                                        
                                                # now stem the synonyms
                                                x = 0
                                                while x < len(synonyms):
                                                        synonyms[x] = stem(synonyms[x]) # stem it
                                                        x += 1
                                                        
                                                for syn in synonyms:
                                                        results = search(str(syn), text) # search the term, and then the text you want to search
                                                        if results == None or results == '' or results == []:
                                                                pass # nothing was found
                                                        else: # means that it has been found
                                                                # 1
                                                                if (word == stem('energy')):
                                                                        foundSubCompOfModel[0] = 1 # found
                                                                if (word == stem('sun')):
                                                                        foundSubCompOfModel[1] = 1 # found)
                                                                if (word == stem('movement')):
                                                                        foundSubCompOfModel[2] = 1 # found
                                                                if (word == stem('transpiration')):
                                                                        foundSubCompOfModel[3] = 1 # found)
                                                                if (word == stem('evaporate')):
                                                                        foundSubCompOfModel[4] = 1 # found)


                                                                if (word == stem('water')):
                                                                        foundSubCompOfModel[5] = 1 # found
                                                                if (word == stem('vapor')):
                                                                        foundSubCompOfModel[6] = 1 # found)
                                                                if (word == stem('atmosphere')):
                                                                        foundSubCompOfModel[7] = 1 # found
                                                                if (word == stem('condense')):
                                                                        foundSubCompOfModel[8] = 1 # found)
                                                                if (word == stem('form')):
                                                                        foundSubCompOfModel[9] = 1 # found)
                                                                if (word == stem('crystallize')):
                                                                        foundSubCompOfModel[10] = 1 # found)
                                                                if (word == stem('snow')):
                                                                        foundSubCompOfModel[11] = 1 # found 
                                                                if (word == stem('ice')):
                                                                        foundSubCompOfModel[12] = 1 # found)
                                                                if (word == stem('gravity')):
                                                                        foundSubCompOfModel[13] = 1 # found


                                                                if (word == stem('gravity')):
                                                                        foundSubCompOfModel[14] = 1 # found)
                                                                if (word == stem('surface')):
                                                                        foundSubCompOfModel[15] = 1 # found
                                                                if (word == stem('water')):
                                                                        foundSubCompOfModel[16] = 1 # found)
                                                                if (word == stem('rivers')):
                                                                        foundSubCompOfModel[17] = 1 # found
                                                                if (word == stem('flow')):
                                                                        foundSubCompOfModel[18] = 1 # found)
                                                                if (word == stem('ocean')):
                                                                        foundSubCompOfModel[19] = 1 # found


                                                                if (word == stem('evaporate')):
                                                                        foundSubCompOfModel[20] = 1 # found)
                                                                if (word == stem('atmosphere')):
                                                                        foundSubCompOfModel[21] = 1 # found)


                                                                if (word == stem('plants')):
                                                                        foundSubCompOfModel[22] = 1 # found)
                                                                if (word == stem('transpiration')):
                                                                        foundSubCompOfModel[23] = 1 # found)
                                                                if (word == stem('decomposition')):
                                                                        foundSubCompOfModel[24] = 1 # found)


                                                                if (word == stem('animals')):
                                                                        foundSubCompOfModel[25] = 1 # found)
                                                                if (word == stem('respiration')):
                                                                        foundSubCompOfModel[26] = 1 # found)
                                                                if (word == stem('decomposition')):
                                                                        foundSubCompOfModel[27] = 1 # found)


                                                                if (word == stem('freeze')):
                                                                        foundSubCompOfModel[28] = 1 # found)
                                                                if (word == stem('crystallize')):
                                                                        foundSubCompOfModel[29] = 1 # found)
                                                                if (word == stem('frozen')):
                                                                        foundSubCompOfModel[30] = 1 # found)
                                                                if (word == stem('form')):
                                                                        foundSubCompOfModel[31] = 1 # found)
                                                                if (word == stem('glaciers')):
                                                                        foundSubCompOfModel[32] = 1 # found)
                                                                if (word == stem('ice')):
                                                                        foundSubCompOfModel[33] = 1 # found)


                                                                if (word == stem('water')):
                                                                        foundSubCompOfModel[34] = 1 # found)
                                                                if (word == stem('below')):
                                                                        foundSubCompOfModel[35] = 1 # found)
                                                                if (word == stem('ground')):
                                                                        foundSubCompOfModel[36] = 1 # found)
                                                                if (word == stem('aquifers')):
                                                                        foundSubCompOfModel[37] = 1 # found)


                                                                if (word == stem('evaporation')):
                                                                        foundSubCompOfModel[38] = 1 # found)
                                                                if (word == stem('transpiration')):
                                                                        foundSubCompOfModel[39] = 1 # found)
                                                                if (word == stem('condensation')):
                                                                        foundSubCompOfModel[40] = 1 # found)
                                                                if (word == stem('crystallization')):
                                                                        foundSubCompOfModel[41] = 1 # found)
                                                                if (word == stem('precipitation')):
                                                                        foundSubCompOfModel[42] = 1 # found)


                                                                if (word == stem('phases')):
                                                                        foundSubCompOfModel[43] = 1 # found)
                                                                if (word == stem('locations')):
                                                                        foundSubCompOfModel[44] = 1 # found)
                                                                if (word == stem('surface')):
                                                                        foundSubCompOfModel[45] = 1 # found)
                                                                if (word == stem('atmosphere')):
                                                                        foundSubCompOfModel[46] = 1 # found)
                                        except: # if there isnt a synonym for the word, we must continue on
                                                results = search(str(word), text) # search the term, and then the text you want to search
                                                if results == None or results == '' or results == []:
                                                        pass # nothing was found
                                                else: # means that it has been found
                                                        if (word == stem('energy')):
                                                                foundSubCompOfModel[0] = 1 # found
                                                        if (word == stem('sun')):
                                                                foundSubCompOfModel[1] = 1 # found)
                                                        if (word == stem('movement')):
                                                                foundSubCompOfModel[2] = 1 # found
                                                        if (word == stem('transpiration')):
                                                                foundSubCompOfModel[3] = 1 # found)
                                                        if (word == stem('evaporate')):
                                                                foundSubCompOfModel[4] = 1 # found)


                                                        if (word == stem('water')):
                                                                foundSubCompOfModel[5] = 1 # found
                                                        if (word == stem('vapor')):
                                                                foundSubCompOfModel[6] = 1 # found)
                                                        if (word == stem('atmosphere')):
                                                                foundSubCompOfModel[7] = 1 # found
                                                        if (word == stem('condense')):
                                                                foundSubCompOfModel[8] = 1 # found)
                                                        if (word == stem('form')):
                                                                foundSubCompOfModel[9] = 1 # found)
                                                        if (word == stem('crystallize')):
                                                                foundSubCompOfModel[10] = 1 # found)
                                                        if (word == stem('snow')):
                                                                foundSubCompOfModel[11] = 1 # found 
                                                        if (word == stem('ice')):
                                                                foundSubCompOfModel[12] = 1 # found)
                                                        if (word == stem('gravity')):
                                                                foundSubCompOfModel[13] = 1 # found


                                                        if (word == stem('gravity')):
                                                                foundSubCompOfModel[14] = 1 # found)
                                                        if (word == stem('surface')):
                                                                foundSubCompOfModel[15] = 1 # found
                                                        if (word == stem('water')):
                                                                foundSubCompOfModel[16] = 1 # found)
                                                        if (word == stem('rivers')):
                                                                foundSubCompOfModel[17] = 1 # found
                                                        if (word == stem('flow')):
                                                                foundSubCompOfModel[18] = 1 # found)
                                                        if (word == stem('ocean')):
                                                                foundSubCompOfModel[19] = 1 # found


                                                        if (word == stem('evaporate')):
                                                                foundSubCompOfModel[20] = 1 # found)
                                                        if (word == stem('atmosphere')):
                                                                foundSubCompOfModel[21] = 1 # found)


                                                        if (word == stem('plants')):
                                                                foundSubCompOfModel[22] = 1 # found)
                                                        if (word == stem('transpiration')):
                                                                foundSubCompOfModel[23] = 1 # found)
                                                        if (word == stem('decomposition')):
                                                                foundSubCompOfModel[24] = 1 # found)


                                                        if (word == stem('animals')):
                                                                foundSubCompOfModel[25] = 1 # found)
                                                        if (word == stem('respiration')):
                                                                foundSubCompOfModel[26] = 1 # found)
                                                        if (word == stem('decomposition')):
                                                                foundSubCompOfModel[27] = 1 # found)


                                                        if (word == stem('freeze')):
                                                                foundSubCompOfModel[28] = 1 # found)
                                                        if (word == stem('crystallize')):
                                                                foundSubCompOfModel[29] = 1 # found)
                                                        if (word == stem('frozen')):
                                                                foundSubCompOfModel[30] = 1 # found)
                                                        if (word == stem('form')):
                                                                foundSubCompOfModel[31] = 1 # found)
                                                        if (word == stem('glaciers')):
                                                                foundSubCompOfModel[32] = 1 # found)
                                                        if (word == stem('ice')):
                                                                foundSubCompOfModel[33] = 1 # found)


                                                        if (word == stem('water')):
                                                                foundSubCompOfModel[34] = 1 # found)
                                                        if (word == stem('below')):
                                                                foundSubCompOfModel[35] = 1 # found)
                                                        if (word == stem('ground')):
                                                                foundSubCompOfModel[36] = 1 # found)
                                                        if (word == stem('aquifers')):
                                                                foundSubCompOfModel[37] = 1 # found)


                                                        if (word == stem('evaporation')):
                                                                foundSubCompOfModel[38] = 1 # found)
                                                        if (word == stem('transpiration')):
                                                                foundSubCompOfModel[39] = 1 # found)
                                                        if (word == stem('condensation')):
                                                                foundSubCompOfModel[40] = 1 # found)
                                                        if (word == stem('crystallization')):
                                                                foundSubCompOfModel[41] = 1 # found)
                                                        if (word == stem('precipitation')):
                                                                foundSubCompOfModel[42] = 1 # found)


                                                        if (word == stem('phases')):
                                                                foundSubCompOfModel[43] = 1 # found)
                                                        if (word == stem('locations')):
                                                                foundSubCompOfModel[44] = 1 # found)
                                                        if (word == stem('surface')):
                                                                foundSubCompOfModel[45] = 1 # found)
                                                        if (word == stem('atmosphere')):
                                                                foundSubCompOfModel[46] = 1 # found)  
                                count += 1
                        
                        # set the found items
                        tester = 0 # this will test all the parts of the array
                        
                        partials = 0 # count the number, if more than half is found might as well add it since nobody will ever match all of these
                        maxloop = 5
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[0] = 1
                                outputToScreen = outputToScreen + '3.a.i.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '3.a.i.: Not Found' + '\n'
                                        
                        partials = 0
                        maxloop = 14
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                outputToScreen = outputToScreen + '3.a.ii.: Found' + '\n'
                                foundCompOfModel[1] = 1
                        else:
                                outputToScreen = outputToScreen + '3.a.ii.: Not Found' + '\n'


                        partials = 0
                        maxloop = 38
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[2] = 1
                                outputToScreen = outputToScreen + '3.a.iii.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '3.a.iii.: Not Found' + '\n'


                        partials = 0
                        maxloop = 43
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[3] = 1
                                outputToScreen = outputToScreen + '3.b.i.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '3.b.i.: Not Found' + '\n'


                        partials = 0
                        maxloop = 47
                        loopsize = 0
                        while tester < maxloop:
                                if foundSubCompOfModel[tester] == 1:
                                        partials += 1
                                tester += 1
                                loopsize += 1
                        if tester > int(loopsize/2):
                                foundCompOfModel[4] = 1
                                outputToScreen = outputToScreen + '3.c.i.: Found' + '\n'
                        else:
                                outputToScreen = outputToScreen + '3.c.i.: Not Found' + '\n'






                        # is it a partial match or non at all?
                        count = 0
                        numfound = 0
                        while count < len(foundCompOfModel):
                                if (foundCompOfModel[count] == 1):
                                        numfound += 1
                                count += 1
                                        
                        if numfound == len(foundCompOfModel):
                                outputToScreen = '6.13.5.A \n' +  '3. Connections: Complete Match \n' + outputToScreen
                        elif numfound > 0 and numfound < len(foundCompOfModel):
                                outputToScreen = '6.13.5.A \n' +  '3. Connections: Partial Match \n' + outputToScreen
                        elif numfound == 0:
                                outputToScreen = '6.13.5.A \n' +  '3. Connections: No Matches Discovered \n' + outputToScreen # no need to output things it didnt find


                        algorithm.append(outputToScreen) # save into array






            
                else:   # if the first one isnt found there is nothing else that needs to be searched
                        algorithm.append('The main criteria for 6.13.5.A has not been found in :' +   str(demFiles[filecounter])  + ' . There is no mention found of a model. No criteria can be met for this page.')    
                #####################################################################END OF 6.13##########################################################################################               
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
                
















        #############################################################################
        ## The final step is to add all of this into a model so it can be displayed
        ## in a different page 
        ############################################################################
        submissionsModel.objects.create(userID = str(userid), user = str(userguy), uploadNum = userfileuploads, 
                                        uploadPath = userData.uploadPath, numberOfFiles = userData.numberOfFiles, 
                                        filenames = userData.filenames)        
                
        # output things to a file as well as a model 
        #os.mkdir('directory name') #### this command for creating directory
        #os.mknod('file name') #### this for creating files
        #os.system('touch filename') ###this is another method for creating file by using unix commands in os modules
        path = str(datPath) # + 'output.txt'

        if not os.path.exists(path):
                os.makedirs(path)

        z = 0
        outline = ''
        filename = 'output' + '.txt'
        with open(os.path.join(path, filename), 'w') as out_file:
                # make the input to the file
                bufferz = 'Science and Engineering Practices:\n'
                z = 0
                outline = ''
                if len(sciEng) > 0:
                        while z < len(sciEng):
                                outline = str(sciEngDisplay[z])
                                bufferz = bufferz + outline + '\n'
                                z += 1
                else:
                        bufferz = bufferz + 'Nothing found in this category.\n'
                
                bufferz = bufferz + '\nDisciplinary Core Ideas:\n'
                z = 0
                outline = ''
                if len(disCore) > 0:
                        while z < len(disCore):
                                outline = str(disCoreDisplay[z])
                                bufferz = bufferz + outline + '\n'
                                z += 1
                else:
                        bufferz = bufferz + 'Nothing found in this category.\n'
                
                bufferz = bufferz + '\nCrosscutting Concepts:\n'
                z = 0
                outline = ''
                if len(crosscutting) > 0:
                        while z < len(crosscutting):
                                outline = str(crosscuttingDisplay[z])
                                bufferz = bufferz + outline + '\n'
                                z += 1
                else:
                        bufferz = bufferz + 'Nothing found in this category.\n'

                bufferz = bufferz + '\nAlgorithm Results:\n'
                z = 0
                outline = ''
                if len(algorithm) > 0:
                        while z < len(algorithm):
                                outline = str(algorithm[z])
                                bufferz = bufferz + outline + '\n'
                                z += 1
                else:
                        bufferz = bufferz + 'Nothing found in this category.\n'

                out_file.write(bufferz) # write the input
                out_file.close() # close the buffer and the file

                

        ###### DEBUG      
        #return HttpResponse(sciEng + disCore + crosscutting + algorithm)
        #return HttpResponse(disCore)
        #return HttpResponse(crosscutting)       


        ############################################################################
        # List all variables here that you would like to be able to display
        # they should be the same names no matter what req is chosen
        ############################################################################
        context = {"STANDARD": str(userData.req), "algorithm": algorithm, "aLength": len(algorithm), "sciEng" : sciEngDisplay, "disCore": disCoreDisplay, "crosscutting" : crosscuttingDisplay, "algorithm": algorithm, "seLength": len(sciEng), "dcLength": len(disCore),"ccLength": len(crosscutting)}
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
        

