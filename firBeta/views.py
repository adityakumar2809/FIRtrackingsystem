from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from datetime import datetime

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
                    fir_object = models.FIR.objects.create(sub_division=ps_record_keeper.sub_division,
                                                           police_station=ps_record_keeper.police_station,
                                                           fir_no=fir_no)
                    if current_status_date == 'XXXXXXX':
                        current_status_date = None
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
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
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
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
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
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
                    models.FIRPhase.objects.create(fir=fir_object, phase_index=1, date_registered=datetime.strptime(date, '%d/%m/%y').strftime('%Y-%m-%d'), under_section=under_section, io_name=io_name, accused_name=accused_name,
                                                   accused_status=accused_status, limitation_period=limitation_period, current_status=current_status, current_status_date=datetime.strptime(current_status_date, '%d/%m/%y').strftime('%Y-%m-%d'))
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
        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                sub_division = form.cleaned_data['sub_division']
                police_station = form.cleaned_data['police_station']
                fir_combined_list = []
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False)
                elif police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False, sub_division__exact=sub_division)
                else:        
                    fir_list = models.FIR.objects.all().filter(is_closed__exact=False, sub_division__exact=sub_division, police_station__exact=police_station)
                for fir in fir_list:
                    fir_phase_list = fir.phases.all()
                    if not fir_phase_list[len(fir_phase_list)-1].current_status in ['Untraced', 'Cancelled']:
                        continue
                    fir_combined_list.append([fir, fir_phase_list])
                form = forms.ChooseLocationForm()
                return render(request, 'firBeta/list_edit_fir_vrk.html', {'fir_list': fir_combined_list, 'form': form})
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
                vrk_sent_back_date = request.POST.get('vrk_sent_back_date', None)

                if phase_pk:
                    fir_phase = models.FIRPhase.objects.get(pk__exact=phase_pk)
                    if vrk_receival_date:
                        fir_phase.vrk_receival_date = datetime.strptime(vrk_receival_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if vrk_status:
                        fir_phase.vrk_status = vrk_status
                    if vrk_status_date:    
                        fir_phase.vrk_status_date = datetime.strptime(vrk_status_date, '%d/%m/%y').strftime('%Y-%m-%d')
                    if vrk_sent_back_date:
                        fir_phase.vrk_sent_back_date = datetime.strptime(vrk_sent_back_date, '%d/%m/%y').strftime('%Y-%m-%d')
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


def load_police_stations_view(request):
    sub_division_pk = request.GET.get('sub_division')
    if sub_division_pk == 'all':
        police_station_list = []
    else:
        police_station_list = loc_models.PoliceStation.objects.filter(sub_division__pk=sub_division_pk).order_by('name')
    return render(request, 'firBeta/load_police_stations.html', {'police_station_list': police_station_list})