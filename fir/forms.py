from django import forms
from location import models as loc_models
from account import models as acc_models
from . import models



class CreateFIRForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['fir_no',
                  'date_created',
                  'io_name',
                  'accused_name',
                  'under_section',
                  'accused_status',
                  'limitation_period',
                  'current_status',
                  ]
        

class UpdateFIRPoliceStationForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['io_name',
                  'accused_name',
                  'under_section',
                  'accused_status',
                  'limitation_period',
                  'current_status',
                  'put_in_ssp_office',
                  'put_in_ssp_office_date',
                  'put_in_court',
                  'put_in_court_date',
                  'received_from_court_date', 
                  'appointed_io',
                  'is_closed',
                  'closed_date'
                  ]


class UpdateFIRVRKForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['ssp_approved',
                  ]


class UpdateFIRSSPForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['ssp_approved',
                  ]


class UpdateFIRCourtForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['received_in_court',
                  'received_in_court_date',
                  'court_status',
                  'reverted_by_court_date',
                  ]


class ChooseLocationForm(forms.Form):

    sub_division_name_list = [u['name'] for u in loc_models.SubDivision.objects.all().values('name')]
    sub_division_pk_list = [u['pk'] for u in loc_models.SubDivision.objects.all().values('pk')]
    SUB_DIVISION_CHOICES = [('','---Select---'), ('all','All')]
    i=0

    for i in range(len(sub_division_name_list)):
        SUB_DIVISION_CHOICES.append((sub_division_pk_list[i], sub_division_name_list[i]))

    sub_division = forms.ChoiceField(choices=SUB_DIVISION_CHOICES) 
    police_station = forms.ChoiceField(choices=[('','---Select Sub Division to choose---')]) 


    def __init__(self, *args, **kwargs):
        super(ChooseLocationForm, self).__init__(*args, **kwargs)
        
        if 'sub_division' in self.data:
            try:
                if(self.data.get('sub_division') == 'all'):
                    self.fields['police_station'] = forms.ChoiceField(choices=[('all','All')])
                else:
                    sub_division_pk = int(self.data.get('sub_division'))

                    police_station_name_list = [u['name'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('name')]
                    police_station_pk_list = [u['pk'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('pk')]
                    POLICE_STATION_CHOICES = [('all','All')]
                    i=0

                    for i in range(len(police_station_name_list)):
                        POLICE_STATION_CHOICES.append((police_station_pk_list[i], police_station_name_list[i]))

                    self.fields['police_station'] = forms.ChoiceField(choices=POLICE_STATION_CHOICES)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
                

class ChoosePoliceStationForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(ChoosePoliceStationForm, self).__init__(*args, **kwargs)
        sub_division_pk = acc_models.DSPRecordKeeper.objects.get(user__pk__exact=user.pk).sub_division.pk
        police_station_name_list = [u['name'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('name')]
        police_station_pk_list = [u['pk'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('pk')]

        POLICE_STATION_CHOICES = [('','---Select---'),('all','All')]
        for i in range(len(police_station_name_list)):
            POLICE_STATION_CHOICES.append((police_station_pk_list[i], police_station_name_list[i]))

        self.fields['police_station'] = forms.ChoiceField(choices=POLICE_STATION_CHOICES)

