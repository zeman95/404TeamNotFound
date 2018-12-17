from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.login, name='login'),
	#path('', views.register, name='register'),
	#path('', views.register.as_view(), name='register'),
	path('profile', auth_views.PasswordChangeView.as_view(), name='profile')
]
