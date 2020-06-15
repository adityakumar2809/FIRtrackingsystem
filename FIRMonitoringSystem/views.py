from django.shortcuts import render, redirect
from location import models as loc_models
from account import models as acc_models
from fir import models as fir_models


def home(request):
    return render(request, 'home.html')


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