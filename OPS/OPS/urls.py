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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from NSR.views import home22 # part of hard coded way, no templates, 1
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ManageUserAccounts.views import home1
from SubHistory.views import home2
from NASSHomeTeacher.views import home4
from UserAccounts.views import login, register, profile
from TLS.views import home10, home11
from django.views.generic.base import TemplateView #for auth tut


# file upload tut https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    
    # this is the hard coded way to do this, attempt 1
    path('NSR/', home22, name = 'home22'),
    path('ManageAccounts/', home1, name = 'home1'),
    path('Submissions/', home2, name = 'home2'),
    path('HomeTeacher/', home4, name='home4'),
    path('', login, name='login'), # changed for auth tut, was '' (the home screen the css is here)
    path('Register/', register, name='register'),
    path('Profile/', profile, name='profile'),
    path('UploadLessonPlans/', home10, name='home10'),
    path('UploadResults/', home11, name='home11'),

    # auth tut
    path('accounts/', include('django.contrib.auth.urls')),
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    
]

# allows images and java files to be added
urlpatterns += staticfiles_urlpatterns()

# file upload tut
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
