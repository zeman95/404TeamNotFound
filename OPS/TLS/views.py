from django.shortcuts import render, HttpResponse
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




# context = {}
#return render(request, 'home10.html', context) this goes after context
"""def home10(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'home10.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'home10.html')"""
def home10(request):
        """form = DocumentForm()
        context = {
                "form": form,
        }"""
        
        if request.method == 'POST':
                form = DocumentForm(request.POST, request.FILES)
                if form.is_valid():
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
        return render(request, 'home11.html', context)

