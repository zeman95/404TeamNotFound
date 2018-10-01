from django.shortcuts import render, HttpResponse

#from django.http import HttpResponse


def home(request):
    	#this is the old way
	#return HttpResponse("<h2>This is the NSR page.</h2>")

	# this is how to do templates
	#return render(request, 'NSR/home.html', {'title': 'Home'})#context)
	context = {}
	return render(request, 'NSR/home.html', context)
