from django.urls import path, include

from . import views

urlpatterns = [
    #path('', views.home10, name='home10'),
    path('', views.Form, name="Form")
    path('', views.home11, name='home11'),

]

"""from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home10, name='home10'),
    path('', views.home11, name='home11'),

]
"""