from django.shortcuts import render, redirect
from location import models as loc_models
from account import models as acc_models
from fir import models as fir_models


def home(request):
    if request.user.is_authenticated:
        police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
        court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]
        dsp_record_keepers = [u['user'] for u in acc_models.DSPRecordKeeper.objects.all().values('user')]
        vrk_record_keepers = [u['user'] for u in acc_models.VRKRecordKeeper.objects.all().values('user')]
        ssp_record_keepers = [u['user'] for u in acc_models.SSPRecordKeeper.objects.all().values('user')]

        if request.user.pk in police_station_record_keepers:
            return redirect('firBeta:list_edit_fir_ps')
        elif request.user.pk in court_record_keepers:
            return redirect('firBeta:list_edit_fir_nc')
        elif request.user.pk in dsp_record_keepers:
            return redirect('firBeta:list_fir_dsp')
        elif request.user.pk in vrk_record_keepers:
            return redirect('firBeta:list_edit_fir_vrk')
        elif request.user.pk in ssp_record_keepers:
            return redirect('firBeta:list_fir_ssp')

    else:
        return redirect('account:login')
    # return render(request, 'home.html')


def fault(request, fault):
    return render(request, 'fault.html', {'fault': fault})


def success(request, msg):
    return render(request, 'success.html', {'msg': msg})


def populate(request):
    police_station_list =  loc_models.PoliceStation.objects.all()

    ''' For making Naib Court Users '''
    '''
    for ps in police_station_list:
        x = ps.name.lower().replace(' ','-')
        user = acc_models.User.objects.create_user(f'nc-{x}', '', 'testpassword')
        acc_models.CourtRecordKeeper.objects.create(user=user, police_station=loc_models.PoliceStation.objects.get(pk__exact=ps.pk), sub_division=ps.sub_division)
    '''
    return redirect('success', msg='Population Successful')