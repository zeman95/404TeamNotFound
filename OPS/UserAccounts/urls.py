from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.login, name='login'),
	#path('', views.register, name='register'),
	#path('', views.register.as_view(), name='register'),
	path('profile', views.profile, name='profile')
]
