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
