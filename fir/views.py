from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.db.models import F
import datetime

from location import models as loc_models
from account import models as acc_models
from . import models, forms, filters
# Create your views here.

get_request_dict = {
    'fir_no': 'FIR No',
    'date_created__gte': 'Date Registered (Lower Limit)',
    'date_created__lte': 'Date Registered (Upper Limit)',
    'io_name__contains': 'IO Name',
    'accused_name__contains': 'Accused Name',
    'under_section__contains': 'Under Section',
    'accused_status': 'Accused Status',
    'limitation_period__gte': 'Limitation Period (Lower Limit)',
    'limitation_period__lte': 'Limitation Period (Upper Limit)',
    'days_to_expire__gte': 'Days to Expire (Lower Limit)',
    'days_to_expire__lte': 'Days to Expire (Upper Limit)',
    'current_status': 'Current Status',
    'put_in_ssp_office': 'Submitted to SSP Office',
    'put_in_ssp_office_date__gte': 'Date of Submission in SSP Office (Lower Limit)',
    'put_in_ssp_office_date__lte': 'Date of Submission in SSP Office (Upper Limit)',
    'ssp_approved': 'SSP Approved',
    'put_in_court': 'Submitted in Court',
    'put_in_court_date__gte': 'Date of Submission in Court (Lower Limit)',
    'put_in_court_date__lte': 'Date of Submission in Court (Upper Limit)',
    'received_in_court': 'Received in Court',
    'received_in_court_date__gte': 'Date of Receiving in Court (Lower Limit)' ,
    'received_in_court_date__lte': 'Date of Receiving in Court (Upper Limit)' ,
    'court_status': 'Court Status' ,
    'reverted_by_court_date__gte': 'Date of reverting from Court (Lower Limit)' ,
    'reverted_by_court_date__lte': 'Date of reverting from Court (Upper Limit)' ,
    'received_from_court_date__gte': 'Date of receiving in Police Station (Lower Limit)' ,
    'received_from_court_date__lte': 'Date of receiving in Police Station (Upper Limit)' ,
    'appointed_io__contains': 'Appointed IO Name',
    'is_closed': 'Closed FIR'
}

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
                return redirect('fir:list_firs_police_station')
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

    prev_path = request.META.get('HTTP_REFERER', '/')
    current_path = request.path
    if prev_path == '/':
        response = '/'
        request.session['response_to_redirect'] = response
    elif not current_path in prev_path:
        response = prev_path
        request.session['response_to_redirect'] = response

    if (request.user.pk in police_station_record_keepers) and (acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station == models.FIR.objects.get(pk__exact=pk).police_station) :
        if request.method == 'POST':
            form = forms.UpdateFIRPoliceStationForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.io_name = form.cleaned_data['io_name']
                fir.accused_name = form.cleaned_data['accused_name']
                fir.under_section = form.cleaned_data['under_section']
                fir.accused_status = form.cleaned_data['accused_status']
                fir.limitation_period = form.cleaned_data['limitation_period']
                fir.current_status = form.cleaned_data['current_status']
                fir.put_in_ssp_office = form.cleaned_data['put_in_ssp_office']
                fir.put_in_ssp_office_date = form.cleaned_data['put_in_ssp_office_date']
                fir.put_in_court = form.cleaned_data['put_in_court']
                fir.put_in_court_date = form.cleaned_data['put_in_court_date']
                fir.received_from_court_date = form.cleaned_data['received_from_court_date']
                fir.appointed_io = form.cleaned_data['appointed_io']
                fir.is_closed = form.cleaned_data['is_closed']
                fir.closed_date = form.cleaned_data['closed_date']
                fir.save()

                if(fir.is_closed):
                    fir_list = models.FIR.objects.all().filter(fir_no__exact=fir.fir_no, police_station__exact=fir.police_station, sub_division__exact=fir.sub_division)
                    for f in fir_list:
                        f.is_closed = True
                        f.closed_date = fir.closed_date
                        f.save()

                response = request.session.get('response_to_redirect', None)
                if response and response != '/':
                    return HttpResponseRedirect(response)
                else:
                    return redirect('fir:list_firs_police_station')
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRPoliceStationForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_police_station.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def update_fir_vrk_view(request, pk, sub_division_pk, police_station_pk):

    vrk_record_keepers = [u['user'] for u in acc_models.VRKRecordKeeper.objects.all().values('user')]

    prev_path = request.META.get('HTTP_REFERER', '/')
    current_path = request.path
    if prev_path == '/':
        response = '/'
        request.session['response_to_redirect'] = response
    elif not current_path in prev_path:
        response = prev_path
        request.session['response_to_redirect'] = response

    if request.user.pk in vrk_record_keepers:
        if request.method == 'POST':
            form = forms.UpdateFIRVRKForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.ssp_approved = form.cleaned_data['ssp_approved']
                fir.save()
                response = request.session.get('response_to_redirect', None)
                if response and response != '/':
                    return HttpResponseRedirect(response)
                else:
                    return redirect('fir:list_firs_vrk_with_param', sub_division_pk = sub_division_pk, police_station_pk = police_station_pk)
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRVRKForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_vrk.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def update_fir_ssp_view(request, pk, sub_division_pk, police_station_pk):

    ssp_record_keepers = [u['user'] for u in acc_models.SSPRecordKeeper.objects.all().values('user')]

    prev_path = request.META.get('HTTP_REFERER', '/')
    current_path = request.path
    if prev_path == '/':
        response = '/'
        request.session['response_to_redirect'] = response
    elif not current_path in prev_path:
        response = prev_path
        request.session['response_to_redirect'] = response

    if request.user.pk in ssp_record_keepers:
        if request.method == 'POST':
            form = forms.UpdateFIRSSPForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.ssp_approved = form.cleaned_data['ssp_approved']
                fir.save()
                response = request.session.get('response_to_redirect', None)
                if response and response != '/':
                    return HttpResponseRedirect(response)
                else:
                    return redirect('fir:list_firs_ssp_with_param', sub_division_pk = sub_division_pk, police_station_pk = police_station_pk)
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

    prev_path = request.META.get('HTTP_REFERER', '/')
    current_path = request.path
    if prev_path == '/':
        response = '/'
        request.session['response_to_redirect'] = response
    elif not current_path in prev_path:
        response = prev_path
        request.session['response_to_redirect'] = response

    if (request.user.pk in court_record_keepers) and (acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station == models.FIR.objects.get(pk__exact=pk).police_station) :
        if request.method == 'POST':
            form = forms.UpdateFIRCourtForm(request.POST)
            if form.is_valid():
                fir = models.FIR.objects.get(pk__exact=pk)
                fir.received_in_court = form.cleaned_data['received_in_court']
                fir.received_in_court_date = form.cleaned_data['received_in_court_date']
                fir.court_status = form.cleaned_data['court_status']
                fir.reverted_by_court_date = form.cleaned_data['reverted_by_court_date']
                fir.save()
                response = request.session.get('response_to_redirect', None)
                if response and response != '/':
                    return HttpResponseRedirect(response)
                else:
                    return redirect('fir:list_firs_court')
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRCourtForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_court.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')

    '''
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
                return redirect('fir:list_firs_court_with_param', sub_division_pk=sub_division_pk, police_station_pk=police_station_pk)
            else:
                return redirect('fault', fault='Input parameters of Update FIR Form are not valid')
        else:
            form = forms.UpdateFIRCourtForm(instance=models.FIR.objects.get(pk__exact=pk))
            return render(request, 'fir/update_fir_court.html', {'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')
    
    '''


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
                                                   date_created=fir_object.date_created,
                                                   io_name=fir_object.appointed_io,
                                                   accused_name=fir_object.accused_name,
                                                   under_section=fir_object.under_section,
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
        
        page = request.GET.get('page', 1)
        paginator = Paginator(fir_list, 60)
        try:
            firs = paginator.page(page)
        except PageNotAnInteger:
            firs = paginator.page(1)
        except EmptyPage:
            firs = paginator.page(paginator.num_pages)
        
        return render(request, 'fir/list_firs_police_station.html', {'fir_list':firs})

    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_dsp_view(request):

    dsp_record_keepers = [u['user'] for u in acc_models.DSPRecordKeeper.objects.all().values('user')]

    if request.user.pk in dsp_record_keepers:

        if request.method == 'POST':
            form = forms.ChoosePoliceStationForm(data = request.POST, user = request.user)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                if police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
                else:
                    fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
                form = forms.ChoosePoliceStationForm(user = request.user)

                request.session['dsp_ps_choice'] = police_station

                page = request.GET.get('page', 1)
                paginator = Paginator(fir_list, 60)
                try:
                    firs = paginator.page(page)
                except PageNotAnInteger:
                    firs = paginator.page(1)
                except EmptyPage:
                    firs = paginator.page(paginator.num_pages)

                return render(request, 'fir/list_firs_dsp.html', {'fir_list':firs, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChoosePoliceStationForm(user = request.user)
            fir_list = []

            if request.GET.get('page', None):
                police_station = request.session.get('dsp_ps_choice', None)
                if police_station:
                    if police_station == 'all':
                        fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
                    else:
                        fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
                
                    page = request.GET.get('page', 1)
                    paginator = Paginator(fir_list, 60)
                    try:
                        firs = paginator.page(page)
                    except PageNotAnInteger:
                        firs = paginator.page(1)
                    except EmptyPage:
                        firs = paginator.page(paginator.num_pages)

                    return render(request, 'fir/list_firs_dsp.html', {'fir_list':firs, 'form':form})

            return render(request, 'fir/list_firs_dsp.html', {'fir_list':fir_list, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_vrk_view(request):

    vrk_record_keepers = [u['user'] for u in acc_models.VRKRecordKeeper.objects.all().values('user')]

    if request.user.pk in vrk_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all()
                elif sub_division != 'all' and police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()

                request.session['vrk_ps_choice'] = police_station
                request.session['vrk_sd_choice'] = sub_division

                page = request.GET.get('page', 1)
                paginator = Paginator(fir_list, 60)
                try:
                    firs = paginator.page(page)
                except PageNotAnInteger:
                    firs = paginator.page(1)
                except EmptyPage:
                    firs = paginator.page(paginator.num_pages)

                return render(request, 'fir/list_firs_vrk.html', {'fir_list':firs, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()
            fir_list = []

            if request.GET.get('page', None):
                police_station = request.session.get('vrk_ps_choice', None)
                sub_division = request.session.get('vrk_sd_choice', None)
                if police_station and sub_division:
                    if sub_division == 'all':
                        fir_list = models.FIR.objects.all()
                    elif sub_division != 'all' and police_station == 'all':
                        fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                    else:
                        fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                
                    page = request.GET.get('page', 1)
                    paginator = Paginator(fir_list, 60)
                    try:
                        firs = paginator.page(page)
                    except PageNotAnInteger:
                        firs = paginator.page(1)
                    except EmptyPage:
                        firs = paginator.page(paginator.num_pages)

                    return render(request, 'fir/list_firs_vrk.html', {'fir_list':firs, 'form':form})

            return render(request, 'fir/list_firs_vrk.html', {'fir_list':fir_list, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_vrk_with_param_view(request, sub_division_pk, police_station_pk):

    vrk_record_keepers = [u['user'] for u in acc_models.VRKRecordKeeper.objects.all().values('user')]

    if request.user.pk in vrk_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all()
                elif sub_division != 'all' and police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()

                request.session['vrk_ps_choice'] = police_station
                request.session['vrk_sd_choice'] = sub_division 

                page = request.GET.get('page', 1)
                paginator = Paginator(fir_list, 60)
                try:
                    firs = paginator.page(page)
                except PageNotAnInteger:
                    firs = paginator.page(1)
                except EmptyPage:
                    firs = paginator.page(paginator.num_pages)                

                return render(request, 'fir/list_firs_vrk.html', {'fir_list':firs, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()

            if request.GET.get('page', None):
                police_station = request.session.get('vrk_ps_choice', None)
                sub_division = request.session.get('vrk_sd_choice', None)
                if police_station and sub_division:
                    if sub_division == 'all':
                        fir_list = models.FIR.objects.all()
                    elif sub_division != 'all' and police_station == 'all':
                        fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                    else:
                        fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
            else:
                fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station_pk, sub_division__pk__exact=sub_division_pk)
            
            page = request.GET.get('page', 1)
            paginator = Paginator(fir_list, 60)
            try:
                firs = paginator.page(page)
            except PageNotAnInteger:
                firs = paginator.page(1)
            except EmptyPage:
                firs = paginator.page(paginator.num_pages)
            
            return render(request, 'fir/list_firs_vrk.html', {'fir_list':firs, 'form':form})
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
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all()
                elif sub_division != 'all' and police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()

                request.session['ssp_ps_choice'] = police_station
                request.session['ssp_sd_choice'] = sub_division

                page = request.GET.get('page', 1)
                paginator = Paginator(fir_list, 60)
                try:
                    firs = paginator.page(page)
                except PageNotAnInteger:
                    firs = paginator.page(1)
                except EmptyPage:
                    firs = paginator.page(paginator.num_pages)

                return render(request, 'fir/list_firs_ssp.html', {'fir_list':firs, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()
            fir_list = []

            if request.GET.get('page', None):
                police_station = request.session.get('ssp_ps_choice', None)
                sub_division = request.session.get('ssp_sd_choice', None)
                if police_station and sub_division:
                    if sub_division == 'all':
                        fir_list = models.FIR.objects.all()
                    elif sub_division != 'all' and police_station == 'all':
                        fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                    else:
                        fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                
                    page = request.GET.get('page', 1)
                    paginator = Paginator(fir_list, 60)
                    try:
                        firs = paginator.page(page)
                    except PageNotAnInteger:
                        firs = paginator.page(1)
                    except EmptyPage:
                        firs = paginator.page(paginator.num_pages)

                    return render(request, 'fir/list_firs_ssp.html', {'fir_list':firs, 'form':form})

            return render(request, 'fir/list_firs_ssp.html', {'fir_list':fir_list, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_ssp_with_param_view(request, sub_division_pk, police_station_pk):

    ssp_record_keepers = [u['user'] for u in acc_models.SSPRecordKeeper.objects.all().values('user')]

    if request.user.pk in ssp_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all()
                elif sub_division != 'all' and police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()

                request.session['ssp_ps_choice'] = police_station
                request.session['ssp_sd_choice'] = sub_division 

                page = request.GET.get('page', 1)
                paginator = Paginator(fir_list, 60)
                try:
                    firs = paginator.page(page)
                except PageNotAnInteger:
                    firs = paginator.page(1)
                except EmptyPage:
                    firs = paginator.page(paginator.num_pages)                

                return render(request, 'fir/list_firs_ssp.html', {'fir_list':firs, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()

            if request.GET.get('page', None):
                police_station = request.session.get('ssp_ps_choice', None)
                sub_division = request.session.get('ssp_sd_choice', None)
                if police_station and sub_division:
                    if sub_division == 'all':
                        fir_list = models.FIR.objects.all()
                    elif sub_division != 'all' and police_station == 'all':
                        fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                    else:
                        fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
            else:
                fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station_pk, sub_division__pk__exact=sub_division_pk)
            
            page = request.GET.get('page', 1)
            paginator = Paginator(fir_list, 60)
            try:
                firs = paginator.page(page)
            except PageNotAnInteger:
                firs = paginator.page(1)
            except EmptyPage:
                firs = paginator.page(paginator.num_pages)
            
            return render(request, 'fir/list_firs_ssp.html', {'fir_list':firs, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')


@login_required
def list_firs_court_view(request):

    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    if request.user.pk in court_record_keepers:
        fir_list = models.FIR.objects.all().filter(police_station__exact=acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station)

        page = request.GET.get('page', 1)
        paginator = Paginator(fir_list, 60)
        try:
            firs = paginator.page(page)
        except PageNotAnInteger:
            firs = paginator.page(1)
        except EmptyPage:
            firs = paginator.page(paginator.num_pages)

        return render(request, 'fir/list_firs_court.html', {'fir_list':firs})

    else:
        return redirect('fault', fault='ACCESS DENIED!')

    '''

    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    if request.user.pk in court_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']

                if sub_division == 'all':
                    fir_list = models.FIR.objects.all()
                elif sub_division != 'all' and police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                else:
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
    
    '''


'''
@login_required
def list_firs_court_with_param_view(request, sub_division_pk, police_station_pk):

    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    if request.user.pk in court_record_keepers:

        if request.method == 'POST':
            form = forms.ChooseLocationForm(request.POST)
            if form.is_valid():
                police_station = form.cleaned_data['police_station']
                sub_division = form.cleaned_data['sub_division']
                if sub_division == 'all':
                    fir_list = models.FIR.objects.all()
                elif sub_division != 'all' and police_station == 'all':
                    fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=sub_division)
                else:
                    fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station, sub_division__pk__exact=sub_division)
                form = forms.ChooseLocationForm()
                return render(request, 'fir/list_firs_court.html', {'fir_list':fir_list, 'form':form})
            else:
                return redirect('fault', fault='Input parameters of Choose Area Form are not valid')
        else:
            form = forms.ChooseLocationForm()
            fir_list = models.FIR.objects.all().filter(police_station__pk__exact=police_station_pk, sub_division__pk__exact=sub_division_pk)
            return render(request, 'fir/list_firs_court.html', {'fir_list':fir_list, 'form':form})
    else:
        return redirect('fault', fault='ACCESS DENIED!')
'''


def load_police_stations_view(request):
    sub_division_pk = request.GET.get('sub_division')
    if sub_division_pk == 'all':
        police_station_list = []
    else:
        police_station_list = loc_models.PoliceStation.objects.filter(sub_division__pk=sub_division_pk).order_by('name')
    return render(request, 'fir/load_police_stations.html', {'police_station_list': police_station_list})


@login_required
def filter_data_view(request):
    dsp_record_keepers = [u['user'] for u in acc_models.DSPRecordKeeper.objects.all().values('user')]
    police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    days_to_expire_lower_limit = request.GET.get('days_to_expire__gte', None)
    days_to_expire_upper_limit = request.GET.get('days_to_expire__lte', None)

    applied_filters = {}
    for key,value in request.GET.items():
        if( value and value != 'unknown'):
            v = value.replace('_',' ').title()
            v = v.replace('True', 'Yes')
            v = v.replace('False', 'No')
            v = v.replace('Po', 'PO')
            applied_filters[get_request_dict[key]] = v

    if request.user.pk in dsp_record_keepers:
        fir_list = models.FIR.objects.all().filter(sub_division__pk__exact=acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division.pk)
        if len(fir_list) > 0:
            if(days_to_expire_lower_limit):
                lower_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_lower_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created >= lower_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)          
            if(days_to_expire_upper_limit):
                upper_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_upper_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created <= upper_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)
            fir_id_list = []
            for i in range(len(fir_list)-1):
                if(fir_list[i].fir_no != fir_list[i+1].fir_no):
                    fir_id_list.append(fir_list[i].pk)
            fir_id_list.append(fir_list[len(fir_list)-1].pk)
            fir_list = fir_list.filter(pk__in = fir_id_list)
        fir_filtered_data = filters.FirFilterSubDivision(request.GET, queryset = fir_list)
    elif request.user.pk in police_station_record_keepers:
        fir_list = models.FIR.objects.all().filter(police_station__exact=acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station)
        if len(fir_list) > 0:
            if(days_to_expire_lower_limit):
                lower_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_lower_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created >= lower_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)          
            if(days_to_expire_upper_limit):
                upper_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_upper_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created <= upper_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)
            fir_id_list = []
            for i in range(len(fir_list)-1):
                if(fir_list[i].fir_no != fir_list[i+1].fir_no):
                    fir_id_list.append(fir_list[i].pk)
            fir_id_list.append(fir_list[len(fir_list)-1].pk)
            fir_list = fir_list.filter(pk__in = fir_id_list)
        fir_filtered_data = filters.FirFilterPoliceStationCourt(request.GET, queryset = fir_list)
    elif request.user.pk in court_record_keepers:
        fir_list = models.FIR.objects.all().filter(police_station__exact=acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station)
        if len(fir_list) > 0:
            if(days_to_expire_lower_limit):
                lower_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_lower_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created >= lower_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)          
            if(days_to_expire_upper_limit):
                upper_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_upper_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created <= upper_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)
            fir_id_list = []
            for i in range(len(fir_list)-1):
                if(fir_list[i].fir_no != fir_list[i+1].fir_no):
                    fir_id_list.append(fir_list[i].pk)
            fir_id_list.append(fir_list[len(fir_list)-1].pk)
            fir_list = fir_list.filter(pk__in = fir_id_list)
        fir_filtered_data = filters.FirFilterPoliceStationCourt(request.GET, queryset = fir_list)
    else:
        fir_list = models.FIR.objects.all()
        if len(fir_list):
            if(days_to_expire_lower_limit):
                lower_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_lower_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created >= lower_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)          
            if(days_to_expire_upper_limit):
                upper_limit = datetime.date.today() + datetime.timedelta(days=int(days_to_expire_upper_limit))
                fir_id_list = []
                for fir in fir_list:
                    if fir.date_created <= upper_limit - datetime.timedelta(fir.limitation_period or 0):
                        fir_id_list.append(fir.pk)
                fir_list = fir_list.filter(pk__in = fir_id_list)
            fir_id_list = []
            for i in range(len(fir_list)-1):
                if(fir_list[i].fir_no != fir_list[i+1].fir_no):
                    fir_id_list.append(fir_list[i].pk)
            fir_id_list.append(fir_list[len(fir_list)-1].pk)
            fir_list = fir_list.filter(pk__in = fir_id_list)
        fir_filtered_data = filters.FirFilterAll(request.GET, queryset = fir_list)

    return render(request, 'fir/list_firs_filtered.html', {'fir_filtered_data': fir_filtered_data, 'days_to_expire_lower_limit_value': days_to_expire_lower_limit, 'days_to_expire_upper_limit_value': days_to_expire_upper_limit, 'applied_filters': applied_filters})


@login_required
def detail_fir_view(request, pk):
    dsp_record_keepers = [u['user'] for u in acc_models.DSPRecordKeeper.objects.all().values('user')]
    police_station_record_keepers = [u['user'] for u in acc_models.PoliceStationRecordKeeper.objects.all().values('user')]
    court_record_keepers = [u['user'] for u in acc_models.CourtRecordKeeper.objects.all().values('user')]

    try:
        fir_object = models.FIR.objects.get(pk__exact=pk)
    except:
        return redirect('fault', fault='The required FIR does not exists!')

    if (request.user.pk in dsp_record_keepers) and not (acc_models.DSPRecordKeeper.objects.get(user__pk__exact=request.user.pk).sub_division == models.FIR.objects.get(pk__exact=pk).sub_division):
        return redirect('fault', fault='ACCESS DENIED!')
    elif (request.user.pk in court_record_keepers) and not (acc_models.CourtRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station == models.FIR.objects.get(pk__exact=pk).police_station):
        return redirect('fault', fault='ACCESS DENIED!')
    elif (request.user.pk in police_station_record_keepers) and not (acc_models.PoliceStationRecordKeeper.objects.get(user__pk__exact=request.user.pk).police_station == models.FIR.objects.get(pk__exact=pk).police_station):
        return redirect('fault', fault='ACCESS DENIED!')

    fir_phase_list = models.FIR.objects.all().filter(fir_no__exact=fir_object.fir_no, police_station__exact=fir_object.police_station, sub_division__exact=fir_object.sub_division)

    return render(request, 'fir/detail_fir.html', {'fir_phase_list':fir_phase_list})
        