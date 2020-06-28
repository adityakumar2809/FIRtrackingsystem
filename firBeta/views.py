from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from account import models as acc_models
from location import models as loc_models
from . import models

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
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=date, under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=current_status_date)
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
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=date, under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=current_status_date)
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
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=date, under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=current_status_date)
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
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no,
                                                           is_closed=True)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=date, under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=current_status_date)
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
def list_edit_fir_vrk_view(request):
    vrk_record_keepers = [u['user'] for u in acc_models.VRKRecordKeeper.objects.all().values('user')]
    if request.user.pk in vrk_record_keepers:
        fir_combined_list = []
        fir_list = models.FIR.objects.all().filter(is_closed__exact=False)
        for fir in fir_list:
            fir_phase_list = fir.phases.all()
            if not fir_phase_list[len(fir_phase_list)-1].current_status in ['Untraced', 'Cancelled']:
                continue
            fir_combined_list.append([fir, fir_phase_list])
        return render(request, 'firBeta/list_edit_fir_vrk.html', {'fir_list': fir_combined_list})
    else:
        return redirect('fault', fault='ACCESS DENIED!')