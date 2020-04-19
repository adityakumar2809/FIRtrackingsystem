from django import forms
from . import models



class CreateFIRForm(forms.ModelForm):

    class Meta():
        model = models.FIR
        fields = ['fir_no','io_name','accused_name','accused_status','limitation_period','current_status']
        


