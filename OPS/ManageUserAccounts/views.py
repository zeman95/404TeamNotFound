from django.shortcuts import render, HttpResponse

def home1(request):
	context = {}
	return render(request, 'home1.html', context)

