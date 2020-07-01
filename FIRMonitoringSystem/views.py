from django.shortcuts import render, redirect
from location import models as loc_models
from account import models as acc_models
from fir import models as fir_models
from firBeta import models as fir_beta_models

import random, datetime


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
    for ps in police_station_list:
        x = 87
        y = random.randint(x,x+12)
        while(x <= y):
            fir_object = fir_beta_models.FIR.objects.create(fir_no = f'{x}/20', sub_division = ps.sub_division, police_station = ps)

            fir_phase = fir_beta_models.FIRPhase.objects.create(fir = fir_object, 
                                                                phase_index = 1, 
                                                                date_registered = datetime.datetime.today() - datetime.timedelta(days=random.randint(1,10)),
                                                                under_section = random.randint(100,200),
                                                                io_name = random.choice(['PQR','STU','VWX','XYZ']),
                                                                accused_name = random.choice(['ABC','DEF','GHI','JKL','MNO']),
                                                                accused_status = random.choice(['Arrested','Not Arrested', 'P.O.']),
                                                                limitation_period = random.randint(10,35),
                                                                current_status = random.choice(['Untraced', 'Cancelled']),
                                                                current_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(1,3))
                                                                )
                                                                
            fir_phase = fir_beta_models.FIRPhase.objects.get(pk__exact = fir_phase.pk)
            if random.choice([True, True, True, True, False]):
                fir_phase.vrk_receival_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(3,4))
                if random.choice([True, True, True, True, False]):
                    fir_phase.vrk_status = 'Approved'
                    fir_phase.vrk_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(4,5))
                    fir_phase.vrk_sent_back_date = datetime.datetime.today()
                    fir_phase.received_from_vrk_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(5,6))
                    if random.choice([True, True, True, False]):
                        fir_phase.put_in_court_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(6,7))
                        if random.choice([True, True, False]):
                            fir_phase.nc_receival_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(7,8))
                            ch = random.choice([1, 2, 3])
                            if ch == 1:
                                fir_phase.nc_status = 'Pending'
                                fir_phase.nc_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(8,9))
                            elif ch == 2:
                                fir_phase.nc_status = 'Approved'
                                fir_phase.nc_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(9, 11))
                            else:
                                fir_phase.nc_status = 'Reinvestigation'
                                fir_phase.nc_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(9, 11))
                else:
                    fir_phase.vrk_status = 'Pending'
                    fir_phase.vrk_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(4,5))
            fir_phase.save()
            x += 1
        
        y = random.randint(x,x+4)
        while(x <= y):
            fir_object = fir_beta_models.FIR.objects.create(fir_no = f'{x}/20', sub_division = ps.sub_division, police_station = ps)
            fir_phase = fir_beta_models.FIRPhase.objects.create(fir = fir_object, 
                                                                phase_index = 1, 
                                                                date_registered = datetime.datetime.today() - datetime.timedelta(days=random.randint(1,10)),
                                                                under_section = random.randint(100,200),
                                                                io_name = random.choice(['PQR','STU','VWX','XYZ']),
                                                                accused_name = random.choice(['ABC','DEF','GHI','JKL','MNO']),
                                                                accused_status = random.choice(['Arrested','Not Arrested', 'P.O.']),
                                                                limitation_period = random.randint(10,35),
                                                                current_status = 'Under Investigation'                                                                
                                                                )
            x += 1
        
        y = random.randint(x,x+4)
        while(x <= y):
            fir_object = fir_beta_models.FIR.objects.create(fir_no = f'{x}/20', sub_division = ps.sub_division, police_station = ps, is_closed = True)
            fir_phase = fir_beta_models.FIRPhase.objects.create(fir = fir_object, 
                                                                phase_index = 1, 
                                                                date_registered = datetime.datetime.today() - datetime.timedelta(days=random.randint(1,10)),
                                                                under_section = random.randint(100,200),
                                                                io_name = random.choice(['PQR','STU','VWX','XYZ']),
                                                                accused_name = random.choice(['ABC','DEF','GHI','JKL','MNO']),
                                                                accused_status = random.choice(['Arrested','Not Arrested', 'P.O.']),
                                                                limitation_period = random.randint(10,35),
                                                                current_status = 'Challan Filed' ,
                                                                current_status_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(1,5))                                                               
                                                                )
            x += 1

    return redirect('success', msg='Population Successful')