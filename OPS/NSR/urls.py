from django.urls import path, include

# this allows you to import the views from the home directory of NSR
from . import views

urlpatterns = [
    # since the main path is already specified, we do not
    # need to specify futher, at this point in the main
    # ops file inside the URLS we already specify './NSR/'
    # so adding here will only append on to that
    path('', views.home, name='home'),
    
    
    #path('', views.home, name='NSR-Home'),
    #path('/', views.home, name='NSR-Home'),
	# add other paths here
]
