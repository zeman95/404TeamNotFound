from django.shortcuts import render, HttpResponse

def home2(request):
	context = {}
	return render(request, 'home2.html', context)


