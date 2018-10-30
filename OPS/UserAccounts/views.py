from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect

#from .forms import CustomUserCreationForm

"""
class Register(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'register.html'
"""

#context = {}
	#return render(request, 'login.html', context)
def login(request):
    return redirect("/accounts/login")
	

def register(request):
	context = {}
	return render(request, 'register.html', context)

def profile(request):
	context = {}
	return render(request, 'profile.html', context)
