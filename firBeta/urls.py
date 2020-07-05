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
    
    path('ajax/load_ps/', views.load_police_stations_view, name='load_police_stations'),
    path('ajax/all_fields_filled/', views.all_fields_filled_view, name='all_fields_filled'),

    path('vrk/', views.list_edit_fir_vrk_view, name='list_edit_fir_vrk'),
    path('vrk/<int:asc>/', views.list_edit_fir_vrk_view, name='list_edit_fir_vrk_asc'),
    path('ajax/edit_fir_save_vrk/', views.edit_fir_save_vrk_ajax_view, name='edit_fir_save_vrk_ajax'),

    path('ps/', views.list_edit_fir_ps_view, name='list_edit_fir_ps'),
    path('ps/<int:asc>/', views.list_edit_fir_ps_view, name='list_edit_fir_ps_asc'),
    path('ajax/edit_fir_save_ps/', views.edit_fir_save_ps_ajax_view, name='edit_fir_save_ps_ajax'),
    path('ajax/edit_fir_save_close_ps/', views.edit_fir_save_close_ps_ajax_view, name='edit_fir_save_close_ps_ajax'),

    path('nc/', views.list_edit_fir_nc_view, name='list_edit_fir_nc'),
    path('nc/<int:asc>/', views.list_edit_fir_nc_view, name='list_edit_fir_nc_asc'),
    path('ajax/edit_fir_save_nc/', views.edit_fir_save_nc_ajax_view, name='edit_fir_save_nc_ajax'),
    path('ajax/edit_fir_save_close_nc/', views.edit_fir_save_close_nc_ajax_view, name='edit_fir_save_close_nc_ajax'),

    path('add-new-phase/<int:pk>/', views.add_new_phase_fir_view, name='add_new_phase_fir'),
    path('ajax/add_new_phase_fir_save/', views.add_new_phase_fir_save_ajax_view, name='add_new_phase_fir_save_ajax'),
    path('ajax/add_new_phase_fir_save_close/', views.add_new_phase_fir_save_close_ajax_view, name='add_new_phase_fir_save_close_ajax'),

    path('dsp/', views.list_fir_dsp_view, name='list_fir_dsp'),
    path('dsp/<int:asc>/', views.list_fir_dsp_view, name='list_fir_dsp_asc'),
    path('dsp/filter/', views.filter_fir_dsp_view, name='filter_fir_dsp'),
    path('dsp/filter/<int:asc>/', views.filter_fir_dsp_view, name='filter_fir_dsp_asc'),

    path('ssp/', views.list_fir_ssp_view, name='list_fir_ssp'),
    path('ssp/<int:asc>/', views.list_fir_ssp_view, name='list_fir_ssp_asc'),
    path('ssp/filter/', views.filter_fir_ssp_view, name='filter_fir_ssp'),
    path('ssp/filter/<int:asc>/', views.filter_fir_ssp_view, name='filter_fir_ssp_asc'),
]