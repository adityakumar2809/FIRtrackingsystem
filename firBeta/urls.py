from django.conf.urls import url
from django.urls import path


from . import views

app_name = 'firBeta'

urlpatterns = [
    path('create/', views.create_fir, name='create'),
    path('ajax/create_fir_save/', views.create_fir_save_ajax_view, name='create_fir_save_ajax'),
    path('ajax/create_fir_save_add/', views.create_fir_save_add_ajax_view, name='create_fir_save_add_ajax'),
    path('ajax/create_fir_save_edit/', views.create_fir_save_edit_ajax_view, name='create_fir_save_edit_ajax'),
    path('ajax/create_fir_save_close/', views.create_fir_save_close_ajax_view, name='create_fir_save_close_ajax'),
    
    path('vrk/', views.list_edit_fir_vrk_view, name='list_edit_fir_vrk'),
    path('ajax/load_ps/', views.load_police_stations_view, name='load_police_stations'),
]