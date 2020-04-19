from django import forms
from . import models



class CreateFIRForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['fir_no',
                  'io_name',
                  'accused_name',
                  'accused_status',
                  'limitation_period',
                  'current_status',
                  ]
        

class UpdateFIRPoliceStationForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['io_name',
                  'accused_name',
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

    