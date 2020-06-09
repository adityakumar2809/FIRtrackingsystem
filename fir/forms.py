from django import forms
from location import models as loc_models
from . import models



class CreateFIRForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['fir_no',
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
                  'put_in_court',
                  'put_in_court_date',
                  'received_from_court_date', 
                  'appointed_io',
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
    SUB_DIVISION_CHOICES = [('','---Select---')]
    i=0

    for i in range(len(sub_division_name_list)):
        SUB_DIVISION_CHOICES.append((sub_division_pk_list[i], sub_division_name_list[i]))

    sub_division = forms.ChoiceField(choices=SUB_DIVISION_CHOICES) 
    police_station = forms.ChoiceField(choices=[('','---Select Sub Division to choose---')]) 


    def __init__(self, *args, **kwargs):
        super(ChooseLocationForm, self).__init__(*args, **kwargs)
        
        if 'sub_division' in self.data:
            try:
                sub_division_pk = int(self.data.get('sub_division'))

                police_station_name_list = [u['name'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('name')]
                police_station_pk_list = [u['pk'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('pk')]
                POLICE_STATION_CHOICES = []
                i=0

                for i in range(len(police_station_name_list)):
                    POLICE_STATION_CHOICES.append((police_station_pk_list[i], police_station_name_list[i]))

                self.fields['police_station'] = forms.ChoiceField(choices=POLICE_STATION_CHOICES)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
                

