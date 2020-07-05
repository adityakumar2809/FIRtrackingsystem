from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail

from datetime import datetime, timedelta

from account import models as acc_models
from location import models as loc_models
from . import models, forms

# Create your views here.


@login_required
def create_fir(request):
    police_station_record_keepers = [
        u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
    if request.user.pk in police_station_record_keepers:
        ps_record_keeper = acc_models.PoliceStationRecordKeeper.objects.get(
            user__pk__exact=request.user.pk)

        return render(request, 'firBeta/create_fir.html', {'current_sub_division': ps_record_keeper.sub_division.name, 'current_police_station': ps_record_keeper.police_station.name})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def create_fir_save_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                fir_no = request.POST.get('fir_no', 'N/A')
                date = request.POST.get('date', 'N/A')
                under_section = request.POST.get('under_section', 'N/A')
                io_name = request.POST.get('io_name', 'N/A')
                accused_name = request.POST.get('accused_name', 'N/A')
                accused_status = request.POST.get('accused_status', 'N/A')
                limitation_period = request.POST.get(
                    'limitation_period', 'N/A')
                current_status = request.POST.get('current_status', 'N/A')
                current_status_date = request.POST.get(
                    'current_status_date', 'N/A')

                if not 'N/A' in [fir_no, date, under_section, io_name, accused_name, accused_status, limitation_period, current_status, current_status_date]:
                    ps_record_keeper = acc_models.PoliceStationRecordKeeper.objects.get(
                        user__pk__exact=request.user.pk)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    else:
                        if datetime.strptime(current_status_date, '%d/%m/%y') < datetime.strptime(date, '%d/%m/%y'):
                            return HttpResponse(5)
                            # return redirect('fault', fault='The date for current status can't be before the date of registration')
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(6)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if datetime.strptime(date, '%d/%m/%y').date() > datetime.today().date():
                        return HttpResponse(6)
                        # return redirect('fault', fault='Future Dates are not permitted')
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
                    else:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status)
                    return HttpResponse(0)
                    # return redirect('success', msg='FIR registered successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Integrity Error


@login_required
def create_fir_save_add_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                fir_no = request.POST.get('fir_no', 'N/A')
                date = request.POST.get('date', 'N/A')
                under_section = request.POST.get('under_section', 'N/A')
                io_name = request.POST.get('io_name', 'N/A')
                accused_name = request.POST.get('accused_name', 'N/A')
                accused_status = request.POST.get('accused_status', 'N/A')
                limitation_period = request.POST.get(
                    'limitation_period', 'N/A')
                current_status = request.POST.get('current_status', 'N/A')
                current_status_date = request.POST.get(
                    'current_status_date', 'N/A')

                if not 'N/A' in [fir_no, date, under_section, io_name, accused_name, accused_status, limitation_period, current_status, current_status_date]:
                    ps_record_keeper = acc_models.PoliceStationRecordKeeper.objects.get(
                        user__pk__exact=request.user.pk)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    else:
                        if datetime.strptime(current_status_date, '%d/%m/%y') < datetime.strptime(date, '%d/%m/%y'):
                            return HttpResponse(5)
                            # return redirect('fault', fault='The date for current status can't be before the date of registration')
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(6)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if datetime.strptime(date, '%d/%m/%y').date() > datetime.today().date():
                        return HttpResponse(6)
                        # return redirect('fault', fault='Future Dates are not permitted')
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
                    else:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status)
                    return HttpResponse(0)
                    # return redirect('success', msg='FIR registered successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Integrity Error


@login_required
def create_fir_save_edit_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                fir_no = request.POST.get('fir_no', 'N/A')
                date = request.POST.get('date', 'N/A')
                under_section = request.POST.get('under_section', 'N/A')
                io_name = request.POST.get('io_name', 'N/A')
                accused_name = request.POST.get('accused_name', 'N/A')
                accused_status = request.POST.get('accused_status', 'N/A')
                limitation_period = request.POST.get(
                    'limitation_period', 'N/A')
                current_status = request.POST.get('current_status', 'N/A')
                current_status_date = request.POST.get(
                    'current_status_date', 'N/A')

                if not 'N/A' in [fir_no, date, under_section, io_name, accused_name, accused_status, limitation_period, current_status, current_status_date]:
                    ps_record_keeper = acc_models.PoliceStationRecordKeeper.objects.get(
                        user__pk__exact=request.user.pk)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    else:
                        if datetime.strptime(current_status_date, '%d/%m/%y') < datetime.strptime(date, '%d/%m/%y'):
                            return HttpResponse(5)
                            # return redirect('fault', fault='The date for current status can't be before the date of registration')
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(6)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if datetime.strptime(date, '%d/%m/%y').date() > datetime.today().date():
                        return HttpResponse(6)
                        # return redirect('fault', fault='Future Dates are not permitted')
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date :
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
                    else:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status)
                    return HttpResponse(0)
                    # return redirect('success', msg='FIR registered successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Integrity Error


@login_required
def create_fir_save_close_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                fir_no = request.POST.get('fir_no', 'N/A')
                date = request.POST.get('date', 'N/A')
                under_section = request.POST.get('under_section', 'N/A')
                io_name = request.POST.get('io_name', 'N/A')
                accused_name = request.POST.get('accused_name', 'N/A')
                accused_status = request.POST.get('accused_status', 'N/A')
                limitation_period = request.POST.get(
                    'limitation_period', 'N/A')
                current_status = request.POST.get('current_status', 'N/A')
                current_status_date = request.POST.get(
                    'current_status_date', 'N/A')

                if not 'N/A' in [fir_no, date, under_section, io_name, accused_name, accused_status, limitation_period, current_status, current_status_date]:
                    ps_record_keeper = acc_models.PoliceStationRecordKeeper.objects.get(
                        user__pk__exact=request.user.pk)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    else:
                        if datetime.strptime(current_status_date, '%d/%m/%y') < datetime.strptime(date, '%d/%m/%y'):
                            return HttpResponse(5)
                            # return redirect('fault', fault='The date for current status can't be before the date of registration')
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(6)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if datetime.strptime(date, '%d/%m/%y').date() > datetime.today().date():
                        return HttpResponse(6)
                        # return redirect('fault', fault='Future Dates are not permitted')
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no,
                                                           is_closed=True)
                    if current_status_date:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
                    else:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=1 , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status)
                    return HttpResponse(0)
                    # return redirect('success', msg='FIR registered successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Integrity Error


@login_required
def list_edit_fir_vrk_view(request, asc = 0):
    vrk_record_keepers = [u['user']
                          for u in acc_models.VRKRecordKeeper.objects.all().values('user')]
    if request.user.pk in vrk_record_keepers:
        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                sub_division = form.cleaned_data['sub_division']
                police_station = form.cleaned_data['police_station']
                fir_combined_list = []
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False)
                elif police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(
                        is_closed__exact=False, sub_division__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False,
                                                               sub_division__exact=sub_division, police_station__exact=police_station)
                    
                try:
                    fir_list = sorted(fir_list, 
                                    key = lambda fir: (
                                                        fir.sub_division.pk,
                                                        fir.police_station.pk,
                                                        -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                        -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                        )
                                    )
                except:
                    pass
                
                for fir in fir_list:
                    fir_phase_list = fir.phases.all()
                    if not fir_phase_list[len(fir_phase_list)-1].current_status in ['Untraced', 'Cancelled']:
                        continue
                    if fir_phase_list[len(fir_phase_list)-1].vrk_sent_back_date:
                        continue
                    fir_combined_list.append([fir, fir_phase_list])
                form = forms.ChooseLocationForm()
                return render(request, 'firBeta/list_edit_fir_vrk.html', {'fir_list': fir_combined_list, 'form': form, 'asc': asc})
            else:
                return redirect('fault', fault='Invalid Parameters!')
        else:
            form = forms.ChooseLocationForm()
            return render(request, 'firBeta/list_edit_fir_vrk.html', {'fir_list': [], 'form': form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def edit_fir_save_vrk_ajax_view(request):
    try:
        if request.method == 'POST':
            vrk_record_keepers = [
                u['user'] for u in acc_models.VRKRecordKeeper.objects.all().values('user')]
            if request.user.pk in vrk_record_keepers:
                phase_pk = request.POST.get('phase_pk', None)
                vrk_receival_date = request.POST.get('vrk_receival_date', None)
                vrk_status = request.POST.get('vrk_status', None)
                vrk_status_date = request.POST.get('vrk_status_date', None)
                vrk_sent_back_date = request.POST.get(
                    'vrk_sent_back_date', None)

                if phase_pk:
                    fir_phase = models.FIRPhase.objects.get(pk__exact=phase_pk)
                    initial_vrk_sent_back_date = fir_phase.vrk_sent_back_date
                    if (not vrk_receival_date) and (vrk_status or vrk_status_date or vrk_sent_back_date):
                        return HttpResponse(5)
                        # return redirect('fault', fault='Cannot process FIR Status untill Receival Date is entered')
                    if vrk_status and (not vrk_status_date):
                        return HttpResponse(6)
                        # return redirect('fault', fault='Enter Date along with status')
                    if (not vrk_status == 'Approved') and vrk_sent_back_date:
                        return HttpResponse(7)
                        # return redirect('fault', fault='FIR cannot be returned before Approving it')

                    if vrk_status_date == 'XXXXXXX':
                        vrk_status_date = None

                    if vrk_receival_date and fir_phase.current_status_date:
                        if datetime.strptime(vrk_receival_date, '%d/%m/%y').date() < fir_phase.current_status_date:
                            return HttpResponse(8)
                            # return redirect('fault', fault='Date of receiving FIR cannot be before date of sending by Police Station')
                    if vrk_status_date and vrk_receival_date:
                        if datetime.strptime(vrk_status_date, '%d/%m/%y') < datetime.strptime(vrk_receival_date, '%d/%m/%y'):
                            return HttpResponse(9)
                            # return redirect('fault', fault='Date of marking status cannot be before the date of receiving it')
                    if vrk_sent_back_date and vrk_status_date:
                        if datetime.strptime(vrk_sent_back_date, '%d/%m/%y') < datetime.strptime(vrk_status_date, '%d/%m/%y'):
                            return HttpResponse(10)
                            # return redirect('fault', fault='Date of sending back the FIR cannot be before its date of marked status')

                    if vrk_receival_date:
                        if datetime.strptime(vrk_receival_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(11)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if vrk_status_date:
                        if datetime.strptime(vrk_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(11)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if vrk_sent_back_date:
                        if datetime.strptime(vrk_sent_back_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(11)
                            # return redirect('fault', fault='Future Dates are not permitted')

                    if vrk_receival_date:
                        fir_phase.vrk_receival_date = datetime.strptime(
                            vrk_receival_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if vrk_status:
                        fir_phase.vrk_status = vrk_status
                    if vrk_status_date:
                        fir_phase.vrk_status_date = datetime.strptime(
                            vrk_status_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if vrk_sent_back_date:
                        fir_phase.vrk_sent_back_date = datetime.strptime(
                            vrk_sent_back_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.save()
                    final_vrk_sent_back_date = fir_phase.vrk_sent_back_date

                    if (not initial_vrk_sent_back_date) and final_vrk_sent_back_date:
                        email_list = [acc_models.PoliceStationRecordKeeper.objects.get(police_station__exact = fir_phase.fir.police_station).user.email]
                        send_mail('FIR File Reverted', f'The FIR file with FIR No. {fir_phase.fir.fir_no} has been approved and reverted from the SSP Office. Kindly check and acknowledge the receival on the online FIR Tracking System.', 'firtrackingsystem.sbsnagar@gmail.com', email_list, fail_silently = True) 

                    return HttpResponse(0)
                    # return redirect('success', msg='FIR edited successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Server Error , Error in save()


@login_required
def list_edit_fir_ps_view(request, asc = 0):
    police_station_record_keepers = [
        u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
    if request.user.pk in police_station_record_keepers:
        fir_list = models.FIR.objects.all().filter(is_closed__exact=False, sub_division__exact=acc_models.PoliceStationRecordKeeper.objects.get(
            user__pk__exact=request.user.pk).sub_division, police_station__exact=acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station)

        try:
            fir_list = sorted(fir_list, 
                            key = lambda fir: (
                                                fir.sub_division.pk,
                                                fir.police_station.pk,
                                                -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                )
                            )
        except:
            pass

        fir_combined_list = []
        for fir in fir_list:
            fir_phase_list = fir.phases.all()
            fir_combined_list.append([fir, fir_phase_list])
        return render(request, 'firBeta/list_edit_fir_ps.html', {'fir_list': fir_combined_list, 'asc': asc})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def edit_fir_save_ps_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                phase_pk = request.POST.get('phase_pk', None)
                io_name = request.POST.get('io_name', None)
                accused_name = request.POST.get('accused_name', None)
                accused_status = request.POST.get('accused_status', None)
                current_status = request.POST.get('current_status', None)
                current_status_date = request.POST.get('current_status_date', None)
                received_from_vrk_date = request.POST.get('received_from_vrk_date', None)
                put_in_court_date = request.POST.get('put_in_court_date', None)
                received_from_nc_date = request.POST.get('received_from_nc_date', None)
                appointed_io = request.POST.get('appointed_io', None)
                appointed_io_date = request.POST.get('appointed_io_date', None)


                if phase_pk:
                    # Add logic to save the fir and also ensure that request is only catered if user is from same ps
                    fir_phase = models.FIRPhase.objects.get(pk__exact=phase_pk)

                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    else:
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() < fir_phase.date_registered:
                            return HttpResponse(12)
                            # return redirect('fault', fault='The date for current status can't be before the date of registration')

                        if fir_phase.phase_index != 1:
                            if datetime.strptime(current_status_date, '%d/%m/%y').date() < models.FIRPhase.objects.get(fir__pk__exact = fir_phase.fir.pk, phase_index__exact = fir_phase.phase_index - 1).appointed_io_date:
                                return HttpResponse(17)
                                # return redirect('fault', fault='Date of current status cannot be before date of appointing the new IO in previous phase')

                    if fir_phase.fir.police_station != acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station:
                        return HttpResponse(2)
                        # return redirect('fault', fault='ACCESS DENIED!')

                    if not (io_name and accused_name and accused_status and current_status):
                        return HttpResponse(5)
                        # return redirect('fault', fault='Missing essential parameters')
                    if current_status != 'Under Investigation' and not current_status_date:
                        return HttpResponse(6)
                        # return redirect('fault', fault='Missing essential parameters')
                    if (not fir_phase.vrk_sent_back_date) and (received_from_vrk_date):
                        return HttpResponse(7)
                        # return redirect('fault', fault='File cannot be received until it is returned from SSP Office')
                    if (put_in_court_date) and (not received_from_vrk_date):
                        return HttpResponse(8)
                        # return redirect('fault', fault='File cannot be submitted in Court before it is received back from SSP Office')
                    if (not fir_phase.nc_sent_back_date) and (received_from_nc_date):
                        return HttpResponse(9)
                        # return redirect('fault', fault='File cannot be received until it is returned from Naib Court')
                    if (not received_from_nc_date) and (appointed_io):
                        return HttpResponse(10)
                        # return redirect('fault', fault='File cannot be marked to new IO before receiving from Naib Court')
                    if ((not appointed_io) and appointed_io_date) or (appointed_io and (not appointed_io_date)):
                        return HttpResponse(11)
                        # return redirect('fault', fault='Please fill Marked IO name along with the date') 

                    if fir_phase.vrk_sent_back_date and received_from_vrk_date:
                        if datetime.strptime(received_from_vrk_date, '%d/%m/%y').date() < fir_phase.vrk_sent_back_date:
                            return HttpResponse(13)
                            # return redirect('fault', fault='The date for receiving the FIR from VRK cannot be before it is sent back from there')

                    if put_in_court_date and received_from_vrk_date:
                        if datetime.strptime(put_in_court_date, '%d/%m/%y') < datetime.strptime(received_from_vrk_date, '%d/%m/%y'):
                            return HttpResponse(14)
                            # return redirect('fault', fault='The date for submitting the FIRin courtcannot be before receiving it from VRK')

                    if fir_phase.nc_sent_back_date and received_from_nc_date:
                        if datetime.strptime(received_from_nc_date, '%d/%m/%y').date() < fir_phase.nc_sent_back_date:
                            return HttpResponse(15)
                            # return redirect('fault', fault='The date for receiving the FIR from Naib Court cannot be before it is sent back from there')

                    if received_from_nc_date and appointed_io_date:
                        if datetime.strptime(appointed_io_date, '%d/%m/%y') < datetime.strptime(received_from_nc_date, '%d/%m/%y'):
                            return HttpResponse(16)
                            # return redirect('fault', fault='The date for marking IO cannot be before the date of receiving the FIR')
                    
                    if current_status_date:
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(18)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if received_from_vrk_date:
                        if datetime.strptime(received_from_vrk_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(18)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if put_in_court_date:
                        if datetime.strptime(put_in_court_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(18)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if received_from_nc_date:
                        if datetime.strptime(received_from_nc_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(18)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if appointed_io_date:
                        if datetime.strptime(appointed_io_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(18)
                            # return redirect('fault', fault='Future Dates are not permitted')


                    fir_phase.io_name = io_name
                    fir_phase.accused_name = accused_name
                    fir_phase.accused_status = accused_status
                    fir_phase.current_status = current_status
                    if current_status_date:
                        fir_phase.current_status_date = datetime.strptime(
                                current_status_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if received_from_vrk_date:
                        fir_phase.received_from_vrk_date = datetime.strptime(
                                received_from_vrk_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if put_in_court_date:
                        fir_phase.put_in_court_date = datetime.strptime(
                                put_in_court_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if received_from_nc_date:
                        fir_phase.received_from_nc_date = datetime.strptime(
                                received_from_nc_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.appointed_io = appointed_io
                    if appointed_io_date:
                        fir_phase.appointed_io_date = datetime.strptime(
                                appointed_io_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.save()
                    

                    return HttpResponse(0)
                    # return redirect('success', msg='FIR edited successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Server Error , Error in save()


@login_required
def edit_fir_save_close_ps_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                phase_pk = request.POST.get('phase_pk', None)
                io_name = request.POST.get('io_name', None)
                accused_name = request.POST.get('accused_name', None)
                accused_status = request.POST.get('accused_status', None)
                current_status = request.POST.get('current_status', None)
                current_status_date = request.POST.get('current_status_date', None)
                received_from_vrk_date = request.POST.get('received_from_vrk_date', None)
                put_in_court_date = request.POST.get('put_in_court_date', None)
                received_from_nc_date = request.POST.get('received_from_nc_date', None)
                appointed_io = request.POST.get('appointed_io', None)
                appointed_io_date = request.POST.get('appointed_io_date', None)

                if phase_pk:
                    # Add logic to save the fir and also ensure that request is only catered if user is from same ps
                    fir_phase = models.FIRPhase.objects.get(pk__exact=phase_pk)
                    if fir_phase.fir.police_station != acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station:
                        return HttpResponse(2)
                        # return redirect('fault', fault='ACCESS DENIED!')


                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    else:
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() < fir_phase.date_registered:
                            return HttpResponse(13)
                            # return redirect('fault', fault='The date for current status can't be before the date of registration')

                        if not fir_phase.phase_index == 1:
                            if datetime.strptime(current_status_date, '%d/%m/%y').date() < models.FIRPhase.objects.get(fir__pk__exact = fir_phase.fir.pk, phase_index__exact = fir_phase.phase_index - 1).appointed_io_date:
                                return HttpResponse(18)
                                # return redirect('fault', fault='Date of current status cannot be before date of appointing the new IO in previous phase')


                    if not (io_name and accused_name and accused_status and current_status):
                        return HttpResponse(5)
                        # return redirect('fault', fault='Missing essential parameters')
                    if current_status != 'Under Investigation' and not current_status_date:
                        return HttpResponse(6)
                        # return redirect('fault', fault='Missing essential parameters')
                    if not current_status == 'Challan Filed':
                        return HttpResponse(12)
                        # return redirect('fault', fault='Status must be Challan Filed to Close FIR')
                    if (not fir_phase.vrk_sent_back_date) and (received_from_vrk_date):
                        return HttpResponse(7)
                        # return redirect('fault', fault='File cannot be received until it is returned from SSP Office')
                    if (put_in_court_date) and (not received_from_vrk_date):
                        return HttpResponse(8)
                        # return redirect('fault', fault='File cannot be submitted in Court before it is received back from SSP Office')
                    if (received_from_nc_date) and (not fir_phase.nc_sent_back_date):
                        return HttpResponse(9)
                        # return redirect('fault', fault='File cannot be received until it is returned from Naib Court')
                    if ((not appointed_io) and appointed_io_date) or (appointed_io and (not appointed_io_date)):
                        return HttpResponse(10)
                        # return redirect('fault', fault='File cannot be marked to new IO before receiving from Naib Court')
                    if (not appointed_io) and appointed_io_date:
                        return HttpResponse(11)
                        # return redirect('fault', fault='Please fill Marked IO name along with the date') 

                    if fir_phase.vrk_sent_back_date and received_from_vrk_date:
                        if datetime.strptime(received_from_vrk_date, '%d/%m/%y').date() < fir_phase.vrk_sent_back_date:
                            return HttpResponse(14)
                            # return redirect('fault', fault='The date for receiving the FIR from VRK cannot be before it is sent back from there')

                    if put_in_court_date and received_from_vrk_date:
                        if datetime.strptime(put_in_court_date, '%d/%m/%y') < datetime.strptime(received_from_vrk_date, '%d/%m/%y'):
                            return HttpResponse(15)
                            # return redirect('fault', fault='The date for submitting the FIRin courtcannot be before receiving it from VRK')

                    if fir_phase.nc_sent_back_date and received_from_nc_date:
                        if datetime.strptime(received_from_nc_date, '%d/%m/%y').date() < fir_phase.nc_sent_back_date:
                            return HttpResponse(16)
                            # return redirect('fault', fault='The date for receiving the FIR from Naib Court cannot be before it is sent back from there')

                    if received_from_nc_date and appointed_io_date:
                        if datetime.strptime(appointed_io_date, '%d/%m/%y') < datetime.strptime(received_from_nc_date, '%d/%m/%y'):
                            return HttpResponse(17)
                            # return redirect('fault', fault='The date for marking IO cannot be before the date of receiving the FIR')

                    if current_status_date:
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(19)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if received_from_vrk_date:
                        if datetime.strptime(received_from_vrk_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(19)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if put_in_court_date:
                        if datetime.strptime(put_in_court_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(19)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if received_from_nc_date:
                        if datetime.strptime(received_from_nc_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(19)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if appointed_io_date:
                        if datetime.strptime(appointed_io_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(19)
                            # return redirect('fault', fault='Future Dates are not permitted')

                    fir_phase.io_name = io_name
                    fir_phase.accused_name = accused_name
                    fir_phase.accused_status = accused_status
                    fir_phase.current_status = current_status
                    if current_status_date:
                        fir_phase.current_status_date = datetime.strptime(
                                current_status_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if received_from_vrk_date:
                        fir_phase.received_from_vrk_date = datetime.strptime(
                                received_from_vrk_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if put_in_court_date:
                        fir_phase.put_in_court_date = datetime.strptime(
                                put_in_court_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if received_from_nc_date:
                        fir_phase.received_from_nc_date = datetime.strptime(
                                received_from_nc_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.appointed_io = appointed_io
                    if appointed_io_date:
                        fir_phase.appointed_io_date = datetime.strptime(
                                appointed_io_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.save()

                    fir = models.FIR.objects.get(pk__exact = fir_phase.fir.pk)
                    fir.is_closed = True
                    fir.save()
                    

                    return HttpResponse(0)
                    # return redirect('success', msg='FIR edited and closed successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Server Error , Error in save()


@login_required
def list_edit_fir_nc_view(request, asc = 0):
    nc_record_keepers = [
        u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]
    if request.user.pk in nc_record_keepers:
        fir_list = models.FIR.objects.all().filter(is_closed__exact=False, sub_division__exact=acc_models.CourtRecordKeeper.objects.get(
            user__pk__exact=request.user.pk).sub_division, police_station__exact=acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station)
        fir_combined_list = []
        
        try:
            fir_list = sorted(fir_list, 
                            key = lambda fir: (
                                                fir.sub_division.pk,
                                                fir.police_station.pk,
                                                -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                )
                            )
        except:
            pass

        for fir in fir_list:
            fir_phase_list = fir.phases.all()
            if not fir_phase_list[len(fir_phase_list)-1].put_in_court_date:
                continue
            if fir_phase_list[len(fir_phase_list)-1].nc_sent_back_date:
                continue
            fir_combined_list.append([fir, fir_phase_list])
        return render(request, 'firBeta/list_edit_fir_nc.html', {'fir_list': fir_combined_list, 'asc':asc})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def edit_fir_save_nc_ajax_view(request):
    try:
        if request.method == 'POST':
            nc_record_keepers = [
                u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]
            if request.user.pk in nc_record_keepers:
                phase_pk = request.POST.get('phase_pk', None)
                nc_receival_date = request.POST.get('nc_receival_date', None)
                nc_status = request.POST.get('nc_status', None)
                nc_status_date = request.POST.get('nc_status_date', None)
                nc_sent_back_date = request.POST.get('nc_sent_back_date', None)

                if phase_pk:
                    # Add logic to save the fir and also ensure that request is only catered if user is from same ps
                    fir_phase = models.FIRPhase.objects.get(pk__exact=phase_pk)
                    nc_sent_back_date_initial = fir_phase.nc_sent_back_date
                    if fir_phase.fir.police_station != acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station:
                        return HttpResponse(2)
                        # return redirect('fault', fault='ACCESS DENIED!')

                    if (not fir_phase.put_in_court_date) and (nc_receival_date):
                        return HttpResponse(5)
                        # return redirect('fault', fault='File cannot be received until it is submitted by Police Station')
                    if (not nc_status and nc_status_date) or (nc_status in ['Approved','Reinvestigation'] and not nc_status_date):
                        return HttpResponse(6)
                        # return redirect('fault', fault='Fill both Status and Date')
                    if (not nc_status == 'Reinvestigation') and nc_sent_back_date:
                        return HttpResponse(7)
                        # return redirect('fault', fault='FIR cannot be returned before marking it for reinvestigation it')

                    if nc_status_date == 'XXXXXXX':
                        nc_status_date = None

                    if fir_phase.put_in_court_date and nc_receival_date:
                        if datetime.strptime(nc_receival_date, '%d/%m/%y').date() < fir_phase.put_in_court_date:
                            return HttpResponse(8)
                            # return redirect('fault', fault='The date for receiving the FIR cannot be before it is sent from the Police Station')
                    if nc_receival_date and nc_status_date:
                        if datetime.strptime(nc_status_date, '%d/%m/%y') < datetime.strptime(nc_receival_date, '%d/%m/%y'):
                            return HttpResponse(9)
                            # return redirect('fault', fault='The date of marking status cannot be before the date of receiving it')
                    if nc_status_date and nc_sent_back_date:
                        if datetime.strptime(nc_sent_back_date, '%d/%m/%y') < datetime.strptime(nc_status_date, '%d/%m/%y'):
                            return HttpResponse(10)
                            # return redirect('fault', fault='The date of sending the FIR back cannot be before the date of marking its status')    

                    if nc_receival_date:
                        if datetime.strptime(nc_receival_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(11)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if nc_status_date:
                        if datetime.strptime(nc_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(11)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if nc_sent_back_date:
                        if datetime.strptime(nc_sent_back_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(11)
                            # return redirect('fault', fault='Future Dates are not permitted')

                    if nc_receival_date:
                        fir_phase.nc_receival_date = datetime.strptime(
                                nc_receival_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.nc_status = nc_status
                    if nc_status_date:
                        fir_phase.nc_status_date = datetime.strptime(
                                nc_status_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if nc_sent_back_date:
                        fir_phase.nc_sent_back_date = datetime.strptime(nc_sent_back_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.save()
                    nc_sent_back_date_final = fir_phase.nc_sent_back_date

                    if (not nc_sent_back_date_initial) and nc_sent_back_date_final:
                        email_list = [acc_models.PoliceStationRecordKeeper.objects.get(police_station__exact = fir_phase.fir.police_station).user.email]
                        send_mail('FIR File Reverted', f'The FIR file with FIR No. {fir_phase.fir.fir_no} has been reverted for reinvestigation from the Naib Court. Kindly check and acknowledge the receival on the online FIR Tracking System.', 'firtrackingsystem.sbsnagar@gmail.com', email_list, fail_silently = True) 
                    

                    return HttpResponse(0)
                    # return redirect('success', msg='FIR edited successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Server Error , Error in save()


@login_required
def edit_fir_save_close_nc_ajax_view(request):
    try:
        if request.method == 'POST':
            nc_record_keepers = [
                u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]
            if request.user.pk in nc_record_keepers:
                phase_pk = request.POST.get('phase_pk', None)
                nc_receival_date = request.POST.get('nc_receival_date', None)
                nc_status = request.POST.get('nc_status', None)
                nc_status_date = request.POST.get('nc_status_date', None)
                nc_sent_back_date = request.POST.get('nc_sent_back_date', None)

                if phase_pk:
                    # Add logic to save the fir and also ensure that request is only catered if user is from same ps
                    fir_phase = models.FIRPhase.objects.get(pk__exact=phase_pk)
                    if fir_phase.fir.police_station != acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station:
                        return HttpResponse(2)
                        # return redirect('fault', fault='ACCESS DENIED!')

                    if (not fir_phase.put_in_court_date) and (nc_receival_date):
                        return HttpResponse(5)
                        # return redirect('fault', fault='File cannot be received until it is submitted by Police Station')
                    if (not nc_status and nc_status_date) or (nc_status in ['Approved','Reinvestigation'] and not nc_status_date):
                        return HttpResponse(6)
                        # return redirect('fault', fault='Fill both Status and Date')
                    if nc_status != 'Approved':
                        return HttpResponse(7)
                        # return redirect('fault', fault='The status must be Approved to Close the FIR')
                    if nc_sent_back_date:
                        return HttpResponse(8)
                        # return redirect('fault', fault='Approved FIRs cannot be returned')

                    if nc_status_date == 'XXXXXXX':
                        nc_status_date = None

                    if fir_phase.put_in_court_date and nc_receival_date:
                        if datetime.strptime(nc_receival_date, '%d/%m/%y').date() < fir_phase.put_in_court_date:
                            return HttpResponse(9)
                            # return redirect('fault', fault='The date for receiving the FIR cannot be before it is sent from the Police Station')
                    if nc_receival_date and nc_status_date:
                        if datetime.strptime(nc_status_date, '%d/%m/%y') < datetime.strptime(nc_receival_date, '%d/%m/%y'):
                            return HttpResponse(10)
                            # return redirect('fault', fault='The date of marking status cannot be before the date of receiving it')
                    if nc_status_date and nc_sent_back_date:
                        if datetime.strptime(nc_sent_back_date, '%d/%m/%y') < datetime.strptime(nc_status_date, '%d/%m/%y'):
                            return HttpResponse(11)
                            # return redirect('fault', fault='The date of sending the FIR back cannot be before the date of marking its status')

                    if nc_receival_date:
                        if datetime.strptime(nc_receival_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(12)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if nc_status_date:
                        if datetime.strptime(nc_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(12)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if nc_sent_back_date:
                        if datetime.strptime(nc_sent_back_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(12)
                            # return redirect('fault', fault='Future Dates are not permitted')

                    if nc_receival_date:
                        fir_phase.nc_receival_date = datetime.strptime(
                                nc_receival_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.nc_status = nc_status
                    if nc_status_date:
                        fir_phase.nc_status_date = datetime.strptime(
                                nc_status_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    fir_phase.save()

                    fir = models.FIR.objects.get(pk__exact = fir_phase.fir.pk)
                    fir.is_closed = True
                    fir.save()
                    

                    return HttpResponse(0)
                    # return redirect('success', msg='FIR edited and closed successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Server Error , Error in save()


@login_required
def  add_new_phase_fir_view(request, pk):
    police_station_record_keepers = [
        u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
    if request.user.pk in police_station_record_keepers:
        try:
            fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
        except:
            return redirect('fault', fault='Invalid data entries!')
        field_names = [f.name for f in models.FIRPhase._meta.get_fields()]

        for field_name in field_names:
            value = getattr(fir_phase, field_name)
            if value in [None, '']:
                return redirect('fault', fault='Fill the entries of previous phase before starting a new one')
        return render(request, 'firBeta/add_new_phase_fir.html', {'fir_phase': fir_phase})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def add_new_phase_fir_save_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                fir_pk = request.POST.get('fir_pk', 'N/A')
                date = request.POST.get('date', 'N/A')
                under_section = request.POST.get('under_section', 'N/A')
                io_name = request.POST.get('io_name', 'N/A')
                accused_name = request.POST.get('accused_name', 'N/A')
                accused_status = request.POST.get('accused_status', 'N/A')
                limitation_period = request.POST.get(
                    'limitation_period', 'N/A')
                current_status = request.POST.get('current_status', 'N/A')
                current_status_date = request.POST.get(
                    'current_status_date', 'N/A')

                if not 'N/A' in [date, under_section, io_name, accused_name, accused_status, limitation_period, current_status, current_status_date]:
                    fir_object = models.FIR.objects.get(pk__exact=fir_pk)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    phase_list = fir_object.phases.all()
                    new_phase_index = len(phase_list)+1
                    if new_phase_index > 3:
                        return HttpResponse(5)
                        # return redirect('fault', fault='More than 3 phases cannot exist')
                    if current_status_date:
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() < phase_list[len(phase_list)-1].appointed_io_date:
                            return HttpResponse(6)
                            # return redirect('fault', fault='Date of current status cannot be before date of appointing the new IO in previous phase')
                        
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(7)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if datetime.strptime(date, '%d/%m/%y').date() > datetime.today().date():
                        return HttpResponse(7)
                        # return redirect('fault', fault='Future Dates are not permitted')
                    else:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=new_phase_index , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status)
                    return HttpResponse(0)
                    # return redirect('success', msg='FIR registered successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Integrity Error


@login_required
def add_new_phase_fir_save_close_ajax_view(request):
    try:
        if request.method == 'POST':
            police_station_record_keepers = [
                u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
            if request.user.pk in police_station_record_keepers:
                fir_pk = request.POST.get('fir_pk', 'N/A')
                date = request.POST.get('date', 'N/A')
                under_section = request.POST.get('under_section', 'N/A')
                io_name = request.POST.get('io_name', 'N/A')
                accused_name = request.POST.get('accused_name', 'N/A')
                accused_status = request.POST.get('accused_status', 'N/A')
                limitation_period = request.POST.get(
                    'limitation_period', 'N/A')
                current_status = request.POST.get('current_status', 'N/A')
                current_status_date = request.POST.get(
                    'current_status_date', 'N/A')

                if not 'N/A' in [date, under_section, io_name, accused_name, accused_status, limitation_period, current_status, current_status_date]:
                    fir_object = models.FIR.objects.get(pk__exact=fir_pk)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    phase_list = fir_object.phases.all()
                    new_phase_index = len(phase_list)+1
                    if new_phase_index > 3:
                        return HttpResponse(5)
                        # return redirect('fault', fault='More than 3 phases cannot exist')
                    if current_status_date:
                        if datetime.strptime(current_status_date, '%d/%m/%y').date() < phase_list[len(phase_list)-1].appointed_io_date:
                            return HttpResponse(6)
                            # return redirect('fault', fault='Date of current status cannot be before date of appointing the new IO in previous phase')

                        if datetime.strptime(current_status_date, '%d/%m/%y').date() > datetime.today().date():
                            return HttpResponse(7)
                            # return redirect('fault', fault='Future Dates are not permitted')
                    if datetime.strptime(date, '%d/%m/%y').date() > datetime.today().date():
                        return HttpResponse(7)
                        # return redirect('fault', fault='Future Dates are not permitted')

                        models.FIRPhase.objects.create(fir=fir_object, phase_index=new_phase_index , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
                    else:
                        models.FIRPhase.objects.create(fir=fir_object, phase_index=new_phase_index , date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                    accused_status=accused_status, limitation_period=limitation_period, current_status=current_status)
                    
                    fir_object.is_closed = True
                    fir_object.save()
                    return HttpResponse(0)
                    # return redirect('success', msg='FIR registered successfully')
                else:
                    return HttpResponse(1)
                    # return redirect('fault', fault='Missing parameters for regstration. Kindly recheck')
            else:
                return HttpResponse(2)
                # return redirect('fault', fault='ACCESS DENIED!')
        else:
            return HttpResponse(3)
            # return redirect('fault', fault='Invalid Operation Requested')
    except:
        return HttpResponse(4)
        # Integrity Error


@login_required
def list_fir_dsp_view(request, asc = 0):
    dsp_record_keepers = [u['user']
                          for u in acc_models.DSPRecordKeeper.objects.all().values('user')]
    if request.user.pk in dsp_record_keepers:
        if request.method == 'POST':
            form = forms.ChoosePoliceStationForm(data = request.POST, user = request.user)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                fir_combined_list = []
                if police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False, sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
                else:
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False, police_station__pk__exact=police_station, sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
                
                try:
                    fir_list = sorted(fir_list, 
                                    key = lambda fir: (
                                                        fir.sub_division.pk,
                                                        fir.police_station.pk,
                                                        -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                        -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                        )
                                    )
                except:
                    pass

                for fir in fir_list:
                    fir_phase_list = fir.phases.all()
                    fir_combined_list.append([fir, fir_phase_list])
                form = forms.ChoosePoliceStationForm(user = request.user)
                return render(request, 'firBeta/list_fir_dsp.html', {'fir_list': fir_combined_list, 'form': form, 'asc':asc})
            else:
                return redirect('fault', fault='Invalid Parameters!')
        else:
            form = forms.ChoosePoliceStationForm(user = request.user)
            return render(request, 'firBeta/list_fir_dsp.html', {'fir_list': [], 'form': form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_fir_ssp_view(request, asc = 0):
    ssp_record_keepers = [u['user']
                          for u in acc_models.SSPRecordKeeper.objects.all().values('user')]
    if request.user.pk in ssp_record_keepers:
        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                sub_division = form.cleaned_data['sub_division']
                police_station = form.cleaned_data['police_station']
                fir_combined_list = []
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False)
                elif police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(
                        is_closed__exact=False, sub_division__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False,
                                                               sub_division__exact=sub_division, police_station__exact=police_station)
                try:
                    fir_list = sorted(fir_list, 
                                    key = lambda fir: (
                                                        fir.sub_division.pk,
                                                        fir.police_station.pk,
                                                        -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                        -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                        )
                                    )
                except:
                    pass

                for fir in fir_list:
                    fir_phase_list = fir.phases.all()
                    fir_combined_list.append([fir, fir_phase_list])
                form = forms.ChooseLocationForm()
                return render(request, 'firBeta/list_fir_ssp.html', {'fir_list': fir_combined_list, 'form': form, 'asc': asc})
            else:
                return redirect('fault', fault='Invalid Parameters!')
        else:
            form = forms.ChooseLocationForm()
            return render(request, 'firBeta/list_fir_ssp.html', {'fir_list': [], 'form': form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def filter_fir_ssp_view(request, asc = 0):
    ssp_record_keepers = [u['user']
                          for u in acc_models.SSPRecordKeeper.objects.all().values('user')]
    if request.user.pk in ssp_record_keepers:
        if request.method == 'POST':
            form = forms.FIRFilterSSPForm(request.POST)
            if form.is_valid():
                sub_division = form.cleaned_data['sub_division']
                police_station = form.cleaned_data['police_station']
                fir_no = form.cleaned_data['fir_no']
                under_section = form.cleaned_data['under_section']
                expiry_date_lower_limit = form.cleaned_data['expiry_date_lower_limit']
                expiry_date_upper_limit = form.cleaned_data['expiry_date_upper_limit']
                is_closed = form.cleaned_data['is_closed']
                fir_combined_list = []

    
                fir_list = models.FIR.objects.all()
                
                try:
                    fir_list = sorted(fir_list, 
                                    key = lambda fir: (
                                                        fir.sub_division.pk,
                                                        fir.police_station.pk,
                                                        -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                        -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                        )
                                    )
                except:
                    pass

                for fir in fir_list:
                    fir_phase_list = fir.phases.all()
                    fir_last_phase = fir_phase_list[len(fir_phase_list)-1]
                    if sub_division:
                        if not (int(sub_division) == fir_last_phase.fir.sub_division.pk):
                            continue
                    if police_station:
                        if not (int(police_station) == fir_last_phase.fir.police_station.pk):
                            continue
                    if fir_no:
                        if not (fir_no == fir_last_phase.fir.fir_no):
                            continue
                    if under_section:
                        if fir_last_phase.under_section.find(under_section) == -1:
                            continue
                    if expiry_date_lower_limit:
                        if (fir_last_phase.date_registered <= datetime.strptime(datetime.strptime(expiry_date_lower_limit, '%d/%m/%y').strftime('%Y-%m-%d'),'%Y-%m-%d').date() - timedelta(fir_last_phase.limitation_period or 0)):
                            continue
                    if expiry_date_upper_limit:
                        if (fir_last_phase.date_registered >= datetime.strptime(datetime.strptime(expiry_date_upper_limit, '%d/%m/%y').strftime('%Y-%m-%d'),'%Y-%m-%d').date() - timedelta(fir_last_phase.limitation_period or 0)):
                            continue
                    if is_closed:
                        if not (bool(is_closed) == fir_last_phase.fir.is_closed):
                            continue
                    fir_combined_list.append([fir, fir_phase_list])

                initial_data = {'sub_division': sub_division,
                                'police_station': police_station,
                                'fir_no': fir_no,
                                'expiry_date_lower_limit':expiry_date_lower_limit,
                                'expiry_date_upper_limit':expiry_date_upper_limit,
                                'is_closed': is_closed
                                }
                form = forms.FIRFilterSSPForm(initial = initial_data)
                return render(request, 'firBeta/filter_fir_ssp.html', {'fir_list': fir_combined_list, 'form': form, 'asc': asc})
            else:
                return redirect('fault', fault='Invalid Parameters!')
        else:
            form = forms.FIRFilterSSPForm()
            return render(request, 'firBeta/filter_fir_ssp.html', {'fir_list': [], 'form': form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def filter_fir_dsp_view(request, asc = 0):
    dsp_record_keepers = [u['user']
                          for u in acc_models.DSPRecordKeeper.objects.all().values('user')]
    if request.user.pk in dsp_record_keepers:
        if request.method == 'POST':
            form = forms.FIRFilterDSPForm(data = request.POST, user = request.user)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                fir_no = form.cleaned_data['fir_no']
                under_section = form.cleaned_data['under_section']
                expiry_date_lower_limit = form.cleaned_data['expiry_date_lower_limit']
                expiry_date_upper_limit = form.cleaned_data['expiry_date_upper_limit']
                is_closed = form.cleaned_data['is_closed']
                fir_combined_list = []

    
                fir_list = models.FIR.objects.all()
                
                try:
                    fir_list = sorted(fir_list, 
                                    key = lambda fir: (
                                                        fir.sub_division.pk,
                                                        fir.police_station.pk,
                                                        -1*int(fir.fir_no[fir.fir_no.index('/')+1:len(fir.fir_no)]), 
                                                        -1*int(fir.fir_no[0:fir.fir_no.index('/')])
                                                        )
                                    )
                except:
                    pass

                for fir in fir_list:
                    fir_phase_list = fir.phases.all()
                    fir_last_phase = fir_phase_list[len(fir_phase_list)-1]
                    if police_station:
                        if not (int(police_station) == fir_last_phase.fir.police_station.pk):
                            continue
                    if fir_no:
                        if not (fir_no == fir_last_phase.fir.fir_no):
                            continue
                    if under_section:
                        if fir_last_phase.under_section.find(under_section) == -1:
                            continue
                    if expiry_date_lower_limit:
                        if (fir_last_phase.date_registered <= datetime.strptime(datetime.strptime(expiry_date_lower_limit, '%d/%m/%y').strftime('%Y-%m-%d'),'%Y-%m-%d').date() - timedelta(fir_last_phase.limitation_period or 0)):
                            continue
                    if expiry_date_upper_limit:
                        if (fir_last_phase.date_registered >= datetime.strptime(datetime.strptime(expiry_date_upper_limit, '%d/%m/%y').strftime('%Y-%m-%d'),'%Y-%m-%d').date() - timedelta(fir_last_phase.limitation_period or 0)):
                            continue
                    if is_closed:
                        if not (bool(is_closed) == fir_last_phase.fir.is_closed):
                            continue
                    fir_combined_list.append([fir, fir_phase_list])

                initial_data = {
                                'police_station': police_station,
                                'fir_no': fir_no,
                                'expiry_date_lower_limit':expiry_date_lower_limit,
                                'expiry_date_upper_limit':expiry_date_upper_limit,
                                'is_closed': is_closed
                                }
                form = forms.FIRFilterDSPForm(initial = initial_data, user = request.user)
                return render(request, 'firBeta/filter_fir_dsp.html', {'fir_list': fir_combined_list, 'form': form, 'asc': asc})
            else:
                return redirect('fault', fault='Invalid Parameters!')
        else:
            form = forms.FIRFilterDSPForm(user = request.user)
            return render(request, 'firBeta/filter_fir_dsp.html', {'fir_list': [], 'form': form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


def load_police_stations_view(request):
    sub_division_pk = request.GET.get('sub_division')
    if sub_division_pk == 'all':
        police_station_list = []
    else:
        police_station_list = loc_models.PoliceStation.objects.filter(
            sub_division__pk=sub_division_pk).order_by('name')
    return render(request, 'firBeta/load_police_stations.html', {'police_station_list': police_station_list})


def all_fields_filled_view(request):
    pk = request.GET.get('phase_pk', None)
    if pk:
        try:
            fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
        except:
            return HttpResponse(1)
        field_names = [f.name for f in models.FIRPhase._meta.get_fields()]

        for field_name in field_names:
            value = getattr(fir_phase, field_name)
            if value in [None, '']:
                return HttpResponse(1)
        return HttpResponse(0)
    else:
        return HttpResponse(1)