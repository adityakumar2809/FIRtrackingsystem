"""FIRMonitoringSystem URL Configuration

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
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fir/', include('fir.urls')),
    path('firBeta/', include('firBeta.urls')),
    path('fault/<str:fault>/', views.fault, name='fault'),
    path('success/<str:msg>/', views.success, name='success'),
    path('send_mails_for_the_day/', views.send_mails_for_the_day, name='send_mails_for_the_day'),
    # path('populate/', views.populate, name='populate'),
    # path('delete/', views.delete, name='delete'),
    # path('change_passwords/', views.change_passwords, name='change_passwords'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
]
