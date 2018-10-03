"""OPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from NSR.views import home # part of hard coded way, no templates, 1
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ManageUserAccounts.views import home1
from SubHistory.views import home2

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # this is the hard coded way to do this, attempt 1
    path('NSR/', home, name = 'home'),
    path('ManageAccounts/', home1, name = 'home1'),
    path('Submissions/', home2, name = 'home2'),
]

# allows images and java files to be added
urlpatterns += staticfiles_urlpatterns()
