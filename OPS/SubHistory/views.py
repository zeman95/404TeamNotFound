from django.shortcuts import render, HttpResponse
import os
from pathlib import Path
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from users.models import CustomUser 
from django.contrib.auth import get_user_model
from TLS.models import submissionsModel
from crum import get_current_user


def home2(request):
	# what do i need: files put into one text file to that I can output what was put into them (last)
	# I need the upload numbers
	# i need the comments
	# i need the submission results

	# always get the user first
	userid = ''
	totaluploadnum = 0
	allcomments = []
	alluploadtexts = [] # this is all the files for input
	allresulttexts = [] # this is all the output files form the alg
	try:
		userguy = get_current_user()
		userid = userguy.id
	except:
		return HttpResponse('You apparently are somehow not logged in - whoops!')

	if userguy.uploads < 1:
		context = {}
		return render(request, 'failure.html', context)
	else:		
		try:
			subModel = submissionsModel.objects.get(userID=str(userid), user = userguy, uploadNum=str(userguy.uploads))
		except:
			return HttpResponse('Could not find that model for that user. Contact system admin for more details')

		# at this point we know the user has uploaded something
		# we also know they have at least one upload, so lets take care of all of them

		x = userguy.uploads
		subtractor = 0
		selectedupload = userguy.uploads
		readInString = ''
		filecounter = 0
		contexts = ''
		# this will give a reverse order
		while x > 0: # loop over all the uploads
			fileselector = ''
			contexts = ''
			selectedupload = selectedupload - subtractor # set which upload we are looking at
			
			subModel = submissionsModel.objects.get(userID=str(userid), user = userguy, uploadNum=str(selectedupload))
			#allcomments.append(str(subModel.comment)) # get the comment from this

			# get the file names from this upload		
			demFiles = subModel.filenames
			demFiles = demFiles.split('#')
			
			# get all the content from the files in that particular upload by looping through all
			filecounter = 0
			readInString = ''
			directory = str(subModel.uploadPath) # get the directory for this upload
			while filecounter < int(subModel.numberOfFiles):
				fileselector = str(directory) + str(demFiles[filecounter]) # get the file path and name, append then for easy reuse and save contents for processing
				f = demFiles[filecounter]

				# get the input from the text file
				with open(fileselector, 'r') as f:
					contents = f.read()
				# append the contents to a continuous string
				readInString = readInString +  '\nFile: ' + str(demFiles[filecounter]) + '\n' + contents + '\n\n-----------------------------------------------------END OF FILE-----------------------------------------------------\n\n'
				filecounter += 1
				#END OF THE FILES LOOP
			
			
			fileselector = str(directory) + 'output.txt'
			# get the input from the text file
			with open(fileselector, 'r') as f:
				contents = f.read()
			
			allresulttexts.append(contents)

			alluploadtexts.append(readInString) # this is all the files for input
			allcomments.append(str(subModel.comment)) # get the comment from this

			subtractor += 1 # make this inc each time since we are going to be getting all of the info for all of the uploads
			x = x-1 # move to the next upload
			# END OF THE UPLOADS LOOP

		

		

			"""
			userID = models.CharField(max_length=512, blank=False)
			uploadNum = models.CharField(max_length=255, blank=False)
			user = models.OneToOneField(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, null=False)
			comment = models.TextField(blank=True) # this needs to be blank when uploaded so that admin can comment
			uploadPath = models.CharField(max_length=512, blank=False)
			numberOfFiles = models.CharField(max_length=512, blank=False)
			filenames = models.CharField(max_length=512, blank=False)
			"""

		#return HttpResponse(alluploadtexts)


	
		context = {}
		return render(request, 'home2.html', context)





	





