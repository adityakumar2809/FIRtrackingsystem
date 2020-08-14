from django.shortcuts import render, redirect
from django.core.mail import send_mail
from location import models as loc_models
from account import models as acc_models
from fir import models as fir_models
from firBeta import models as fir_beta_models

import random, datetime


def home(request):

    last_mail_dates = fir_beta_models.LastMailDate.objects.all()
    flag = 0

    if len(last_mail_dates) == 0:
        flag = 1

    for last_mail_date in last_mail_dates:
        if last_mail_date.date == datetime.date.today():
            flag = 1
            break

    if flag == 0:
        firs = fir_beta_models.FIR.objects.all()
        for fir in firs:
            fir_phase_list = fir.phases.all()
            fir_last_phase = fir_phase_list[len(fir_phase_list)-1]

            if fir_last_phase.fir.is_closed == True:
                continue
            if fir_last_phase.phase_index == 1:
                time_diff = (datetime.date.today() - fir_last_phase.date_registered).days
            else:
                fir_prev_phase = fir_beta_models.FIRPhase.objects.get(fir__exact = fir_last_phase.fir, phase_index__exact = fir_last_phase.phase_index - 1)
                time_diff = (datetime.date.today() - fir_prev_phase.appointed_io_date).days
            
            if time_diff == 20:
                email_list = [acc_models.PoliceStationRecordKeeper.objects.get(police_station__exact = fir_last_phase.fir.police_station).user.email]
                send_mail('Deadline Approaching', f'The FIR file with FIR No. {fir_last_phase.fir.fir_no} has only 20 days left before the expiration of Challan to Court limitation period. Kindly check and take necessary actions.', 'firtrackingsystem.sbsnagar@gmail.com', email_list, fail_silently = True) 
            elif time_diff == 10:
                email_list = [acc_models.PoliceStationRecordKeeper.objects.get(police_station__exact = fir_last_phase.fir.police_station).user.email]
                send_mail('Deadline Approaching', f'The FIR file with FIR No. {fir_last_phase.fir.fir_no} has only 10 days left before the expiration of Challan to Court limitation period. Kindly check and take necessary actions.', 'firtrackingsystem.sbsnagar@gmail.com', email_list, fail_silently = True) 
            elif time_diff == 5:
                email_list = [acc_models.PoliceStationRecordKeeper.objects.get(police_station__exact = fir_last_phase.fir.police_station).user.email]
                send_mail('Deadline Approaching', f'The FIR file with FIR No. {fir_last_phase.fir.fir_no} has only 5 days left before the expiration of Challan to Court limitation period. Kindly check and take necessary actions.', 'firtrackingsystem.sbsnagar@gmail.com', email_list, fail_silently = True) 
            elif time_diff == 0:
                email_list = [acc_models.PoliceStationRecordKeeper.objects.get(police_station__exact = fir_last_phase.fir.police_station).user.email]
                send_mail('Deadline Approaching', f'The FIR file with FIR No. {fir_last_phase.fir.fir_no} has only taday\'s time left before the expiration of Challan to Court limitation period. Kindly check and take necessary actions.', 'firtrackingsystem.sbsnagar@gmail.com', email_list, fail_silently = True) 

        for last_mail_date in last_mail_dates:
            last_mail_date.delete()
            
        fir_beta_models.LastMailDate.objects.create()
    
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
            return redirect('account:logout')
    else:
        return redirect('account:login')
    # return render(request, 'home.html')


def fault(request, fault):
    return render(request, 'fault.html', {'fault': fault})


def success(request, msg):
    return render(request, 'success.html', {'msg': msg})


def populate(request):
    ps = loc_models.PoliceStation.objects.get(name__iexact = 'City NSR')

    x = 19
    fir_object = fir_beta_models.FIR.objects.create(fir_no = f'{x}/20', sub_division = ps.sub_division, police_station = ps)

    accused_name = random.choice(['Aman', 'Sahid', 'Kamlesh', 'Kirti', 'Lokesh', 'Suresh', 'Amrish', 'Palak', 'Kajal'])
    temp = random.choice(['Arrested','Not Arrested', 'P.O.'])
    accused_status = f'{accused_name} - {temp}'
    fir_phase = fir_beta_models.FIRPhase.objects.create(fir = fir_object, 
                                                        phase_index = 1, 
                                                        date_registered = datetime.date(2020, 7, 3),
                                                        under_section = random.randint(100,200),
                                                        io_name = random.choice(['Raj','Kabir','Anand','Manik']),
                                                        accused_name = accused_name,
                                                        accused_status = accused_status,
                                                        limitation_period = 90,
                                                        current_status = 'Under Investigation'
                                                        )

    return redirect('success', msg='Population Successful')


""" def populate(request):
    police_station_list =  loc_models.PoliceStation.objects.all()
    for ps in police_station_list:
        x = 1
        y = random.randint(x,x+12)
        while(x <= y):
            fir_object = fir_beta_models.FIR.objects.create(fir_no = f'{x}/20', sub_division = ps.sub_division, police_station = ps)

            date_registered = datetime.datetime.today() - datetime.timedelta(days=random.randint(1,60))
            current_status_date = date_registered + datetime.timedelta(days=random.randint(1,10))

            fir_phase = fir_beta_models.FIRPhase.objects.create(fir = fir_object, 
                                                                phase_index = 1, 
                                                                date_registered = date_registered,
                                                                under_section = random.randint(100,200),
                                                                io_name = random.choice(['PQR','STU','VWX','XYZ']),
                                                                accused_name = random.choice(['ABC','DEF','GHI','JKL','MNO']),
                                                                accused_status = random.choice(['Arrested','Not Arrested', 'P.O.']),
                                                                limitation_period = random.randint(55,90),
                                                                current_status = random.choice(['Untraced', 'Cancelled']),
                                                                current_status_date = current_status_date
                                                                )
                                                                
            fir_phase = fir_beta_models.FIRPhase.objects.get(pk__exact = fir_phase.pk)
            if random.choice([True, True, True, True, False]):
                vrk_receival_date = current_status_date + datetime.timedelta(days=random.randint(1,10))
                fir_phase.vrk_receival_date = vrk_receival_date
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

        break

    return redirect('success', msg='Population Successful') """