from django.shortcuts import render, HttpResponse

#from django.http import HttpResponse


def home4(request):
    	#this is the old way
	#return HttpResponse("<h2>This is the NSR page.</h2>")

	# this is how to do templates try 1
	#return render(request, 'NSR/home.html', {'title': 'Home'})#context)
	
	# templates try 2
	context = {}
	return render(request, 'home4.html', context)

