from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
from django import forms

from users.forms import CustomUserCreationForm, CustomUserChangeForm # custom user tut
from users.models import CustomUser
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

# def profile(request):
# 	context = {}
# 	return render(request, 'profile.html', context)


class profile(generic.UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'profile.html'

    def get_object(self):
        # CustomUserChangeForm.clean_email(CustomUser)
        # CustomUserChangeForm.clean_username(CustomUser)
        return CustomUser.objects.all().first()

# def profile(request):
#     if request.method == "POST":
#         form = CustomUserChangeForm(data=request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#         else:
#             form = CustomUserChangeForm()
#
#     return render(request, 'profile.html', {'form': form})

