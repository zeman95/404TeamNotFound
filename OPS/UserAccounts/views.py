from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect

from users.forms import CustomUserCreationForm # custom user tut
#from UserAccounts.views import login

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
	

"""def register(request):
	context = {}
	return render(request, 'register.html', context)"""

class register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

def profile(request):
	context = {}
	return render(request, 'profile.html', context)
