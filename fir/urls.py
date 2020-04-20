from django.conf.urls import url
from django.urls import path


from . import views

app_name = 'fir'

urlpatterns = [
    path('create_fir/', views.create_fir_view, name='create_fir'),
    path('update_fir_ps/<int:pk>', views.update_fir_police_station_view, name='update_fir_police_station'),
    path('update_fir_ssp/<int:pk>', views.update_fir_ssp_view, name='update_fir_ssp'),
    path('update_fir_court/<int:pk>', views.update_fir_court_view, name='update_fir_court'),
    path('add_new_phase/<int:pk>', views.add_new_phase_view, name='add_new_phase'),
    path('list_firs_police_station/', views.list_firs_police_station_view, name='list_firs_police_station'),
    path('list_firs_ssp/', views.list_firs_ssp_view, name='list_firs_ssp'),
    path('list_firs_court/', views.list_firs_court_view, name='list_firs_court'),
    path('ajax/load_ps/', views.load_police_stations_view, name='load_police_stations'),
]
