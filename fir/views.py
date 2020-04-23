from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from location import models as loc_models
from account import models as acc_models
from . import models, forms
# Create your views here.

@login_required
def create_fir_view(request):

    police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]

    if request.user.pk in police_station_record_keepers:
        if request.method == 'POST':
            form = forms.CreateFIRForm(request.POST)
            if form.is_valid():
                fir = form.save(commit=False)
                fir.phase = 1
                ps_record_keeper = acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk)
                fir.sub_division = ps_record_keeper.sub_division 
                fir.police_station = ps_record_keeper.police_station
                fir.save()
                return redirect('success', msg='FIR Successfully created')
            else:
                return redirect('fault', fault='Input parameters of Create FIR Form are not valid')
        else:
            form = forms.CreateFIRForm()
            return render(request, 'fir/create_fir.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def update_fir_police_station_view(request, pk):

    police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]

    if (request.user.pk in police_station_record_keepers) and (acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station == models.FIR.objects.get(pk__exact=pk).police_station) :
        if request.method == 'POST':
            form = forms.UpdateFIRPoliceStationForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.io_name = form.cleaned_data['io_name']
                fir.accused_name = form.cleaned_data['accused_name']
                fir.accused_status = form.cleaned_data['accused_status']
                fir.limitation_period = form.cleaned_data['limitation_period']
                fir.current_status = form.cleaned_data['current_status']
                fir.put_in_court = form.cleaned_data['put_in_court']
                fir.put_in_court_date = form.cleaned_data['put_in_court_date']
                fir.received_from_court_date = form.cleaned_data['received_from_court_date']
                fir.appointed_io = form.cleaned_data['appointed_io']
                fir.save()
                return redirect('fir:list_firs_police_station')
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRPoliceStationForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_police_station.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def update_fir_ssp_view(request, pk):

    ssp_record_keepers = [u['user'] for u in acc_models.SSPRecordKeeper.objects.all().values('user')]

    if request.user.pk in ssp_record_keepers:
        if request.method == 'POST':
            form = forms.UpdateFIRSSPForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.ssp_approved = form.cleaned_data['ssp_approved']
                fir.save()
                return redirect('fir:list_firs_ssp')
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRSSPForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_ssp.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def update_fir_court_view(request, pk):

    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    if request.user.pk in court_record_keepers:
        if request.method == 'POST':
            form = forms.UpdateFIRCourtForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.received_in_court = form.cleaned_data['received_in_court']
                fir.received_in_court_date = form.cleaned_data['received_in_court_date']
                fir.court_status = form.cleaned_data['court_status']
                fir.reverted_by_court_date = form.cleaned_data['reverted_by_court_date']
                fir.save()
                return redirect('success', msg='FIR Updated Successfully')
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRCourtForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_court.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def add_new_phase_view(request, pk):

    police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]

    if (request.user.pk in police_station_record_keepers) and (acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station == models.FIR.objects.get(pk__exact=pk).police_station):
        fir_object = models.FIR.objects.get(pk__exact=pk)
        fir_phase_list = models.FIR.objects.all().filter(fir_no__exact=fir_object.fir_no, police_station__exact=fir_object.police_station, sub_division__exact=fir_object.sub_division)

        fir_object = models.FIR.objects.get(fir_no__exact=fir_object.fir_no, phase__exact=len(fir_phase_list), police_station__exact=fir_object.police_station, sub_division__exact=fir_object.sub_division)

        if len(fir_phase_list)==3:
            return redirect('fault', fault='Not more than 3 phases of an FIR could exist')

        fir_object_new = models.FIR.objects.create(sub_division=fir_object.sub_division,
                                                   police_station=fir_object.police_station,
                                                   fir_no=fir_object.fir_no,
                                                   phase=len(fir_phase_list)+1,
                                                   io_name=fir_object.appointed_io,
                                                   accused_name=fir_object.accused_name,
                                                   accused_status=fir_object.accused_status,
                                                   )
        return redirect('fir:update_fir_police_station', pk=fir_object_new.pk)
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_police_station_view(request):

    police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]

    if request.user.pk in police_station_record_keepers:
        fir_list = models.FIR.objects.all().filter(police_station__exact=acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station)
        return render(request, 'fir/list_firs_police_station.html', {'fir_list':fir_list})

    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_ssp_view(request):

    ssp_record_keepers = [u['user'] for u in acc_models.SSPRecordKeeper.objects.all().values('user')]

    if request.user.pk in ssp_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']
                fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()
                return render(request, 'fir/list_firs_ssp.html', {'fir_list':fir_list, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()
            fir_list = []
            return render(request, 'fir/list_firs_ssp.html', {'fir_list':fir_list, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_court_view(request):

    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    if request.user.pk in court_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']
                fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()
                return render(request, 'fir/list_firs_court.html', {'fir_list':fir_list, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()
            fir_list = []
            return render(request, 'fir/list_firs_court.html', {'fir_list':fir_list, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


def load_police_stations_view(request):
    sub_division_pk = request.GET.get('sub_division')
    police_station_list = loc_models.PoliceStation.objects.filter(sub_division__pk=sub_division_pk).order_by('name')
    return render(request, 'fir/load_police_stations.html', {'police_station_list': police_station_list})


def load_police_stations_mat_view(request):
    sub_division_pk = request.GET.get('sub_division')
    mat_dropdown_ul_id = request.GET.get('mat_dropdown_ul_id')
    police_station_list = loc_models.PoliceStation.objects.filter(sub_division__pk=sub_division_pk).order_by('name')
    return render(request, 'fir/load_police_stations_mat.html', {'police_station_list': police_station_list, 'mat_dropdown_ul_id':mat_dropdown_ul_id})