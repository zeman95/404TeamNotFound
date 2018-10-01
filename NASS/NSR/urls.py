from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='NSR-Home'),
    #path('/', views.home, name='NSR-Home'),
	# add other paths here
]
