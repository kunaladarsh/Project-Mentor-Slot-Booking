"""
URL configuration for MentorSlotBooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from myapp.views import loginaction
from myapp.views import signupaction
from myapp.views import homeaction
from myapp.views import editaction
from myapp.views import senddetails
from myapp.views import requestaction
from myapp.views import slotbookingaction

from myapp.views import loginactionteacher
from myapp.views import teachernewrequests
from myapp.views import slotaccepted
from myapp.views import teacherhomeaction
from myapp.views import teachereditrequest



urlpatterns = [
   
    path('',loginaction, name='home'),
    path('signup/', signupaction),
    path('editProfile/', editaction),
    path('senddetails/', senddetails),
    path('requestdetails/', requestaction),
    path('SlotBooking/', slotbookingaction),   
    path('Home/', homeaction),   

    path('teacherhome/', loginactionteacher), 
    path('request/', teachernewrequests), 
    path('slotaccepted/', slotaccepted),
    path('homePage/', teacherhomeaction),   
    path('teachereditProfile/', teachereditrequest),   
   
  
  


]
