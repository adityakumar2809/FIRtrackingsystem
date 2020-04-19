from django.conf.urls import url
from django.urls import path


from . import views

app_name = 'fir'

urlpatterns = [
    path('create_fir/', views.create_fir_view, name='create_fir')
]
