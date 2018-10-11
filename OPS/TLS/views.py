from django.shortcuts import render, HttpResponse

def home10(request):
        context = {}
        return render(request, 'home10.html', context)

def home11(request):
        context = {}
        return render(request, 'home11.html', context)
