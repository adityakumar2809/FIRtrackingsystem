from django import forms
from location import models as loc_models
from account import models as acc_models
from . import models

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


class FIRFilterSSPForm(forms.Form):

    sub_division_name_list = [u['name'] for u in loc_models.SubDivision.objects.all().values('name')]
    sub_division_pk_list = [u['pk'] for u in loc_models.SubDivision.objects.all().values('pk')]
    i=0
    SUB_DIVISION_CHOICES = [(None,'---Select---')]

    for i in range(len(sub_division_name_list)):
        SUB_DIVISION_CHOICES.append((sub_division_pk_list[i], sub_division_name_list[i]))

    police_station_name_list = [u['name'] for u in loc_models.PoliceStation.objects.all().values('name')]
    police_station_pk_list = [u['pk'] for u in loc_models.PoliceStation.objects.all().values('pk')]
    i=0
    POLICE_STATION_CHOICES = [(None,'---Select---')]

    for i in range(len(police_station_name_list)):
        POLICE_STATION_CHOICES.append((police_station_pk_list[i], police_station_name_list[i]))

    # FIR_CLOSED_CHOICES = [(None,'---Select---'),(True,'Yes'),(False,'No')]
    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('91-180', '3 months to 6 months'), ('181-365', '6 months to 1 year'), ('366-730', '1 year to 2 years'), ('731-1825','2 years to 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('next-5', 'Next 5 days'), ('next-10', 'Next 10 days'), ('next-20', 'Next 20 days'), ('next-30', 'Next Month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    VRK_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('5-10','5 days to 10 days'), ('11-30','11 days to 30 days'), ('31-inf','More than 30 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('5-10','5 days to 10 days'), ('11-30','11 days to 30 days'), ('31-inf','More than 30 days')]

    sub_division = forms.ChoiceField(required=False, choices=SUB_DIVISION_CHOICES)
    police_station = forms.ChoiceField(required=False, choices=POLICE_STATION_CHOICES)

    # expiry_date_lower_limit = forms.CharField(required=False)
    # expiry_date_upper_limit = forms.CharField(required=False)

    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_approval_pendency = forms.ChoiceField(required=False, choices=VRK_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)

    # is_closed = forms.ChoiceField(required=False, choices=FIR_CLOSED_CHOICES)


class FIRFilterDSPForm(forms.Form):

    POLICE_STATION_CHOICES = [(None,'---Select---')]

    FIR_CLOSED_CHOICES = [(None,'---Select---'),(True,'Yes'),(False,'No')]

    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('91-180', '3 months to 6 months'), ('181-365', '6 months to 1 year'), ('366-730', '1 year to 2 years'), ('731-1825','2 years to 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('next-5', 'Next 5 days'), ('next-10', 'Next 10 days'), ('next-20', 'Next 20 days'), ('next-30', 'Next Month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('1-2','1 day to 2 days'), ('3-5','3 days to 5 days'), ('6-inf','More than 5 days')]
    VRK_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('5-10','5 days to 10 days'), ('11-30','11 days to 30 days'), ('31-inf','More than 30 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('5-10','5 days to 10 days'), ('11-30','11 days to 30 days'), ('31-inf','More than 30 days')]


    police_station = forms.ChoiceField(required=False, choices=POLICE_STATION_CHOICES)

    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_approval_pendency = forms.ChoiceField(required=False, choices=VRK_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)


    def __init__(self, user, *args, **kwargs):
        super(FIRFilterDSPForm, self).__init__(*args, **kwargs)
        sub_division_pk = acc_models.DSPRecordKeeper.objects.get(user__pk__exact=user.pk).sub_division.pk
        police_station_name_list = [u['name'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('name')]
        police_station_pk_list = [u['pk'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('pk')]

        POLICE_STATION_CHOICES = [(None,'---Select---')]
        for i in range(len(police_station_name_list)):
            POLICE_STATION_CHOICES.append((police_station_pk_list[i], police_station_name_list[i]))

        self.fields['police_station'] = forms.ChoiceField(required=False, choices=POLICE_STATION_CHOICES)


class SSPDashboardForm(forms.Form):

    sub_division_name_list = [u['name'] for u in loc_models.SubDivision.objects.all().values('name')]
    sub_division_pk_list = [u['pk'] for u in loc_models.SubDivision.objects.all().values('pk')]
    SUB_DIVISION_CHOICES = [('','---Select---'), ('all','All')]
    i=0

    for i in range(len(sub_division_name_list)):
        SUB_DIVISION_CHOICES.append((sub_division_pk_list[i], sub_division_name_list[i]))

    sub_division = forms.ChoiceField(choices=SUB_DIVISION_CHOICES) 
    police_station = forms.ChoiceField(choices=[('','---Select Sub Division to choose---')])
    start_date = forms.CharField() 
    end_date = forms.CharField() 


    def __init__(self, *args, **kwargs):
        super(SSPDashboardForm, self).__init__(*args, **kwargs)
        
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


class DSPDashboardForm(forms.Form):

    start_date = forms.CharField() 
    end_date = forms.CharField()
    
    def __init__(self, user, *args, **kwargs):
        super(DSPDashboardForm, self).__init__(*args, **kwargs)
        sub_division_pk = acc_models.DSPRecordKeeper.objects.get(user__pk__exact=user.pk).sub_division.pk
        police_station_name_list = [u['name'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('name')]
        police_station_pk_list = [u['pk'] for u in loc_models.PoliceStation.objects.all().filter(sub_division__pk__exact=sub_division_pk).values('pk')]

        POLICE_STATION_CHOICES = [('','---Select---'),('all','All')]
        for i in range(len(police_station_name_list)):
            POLICE_STATION_CHOICES.append((police_station_pk_list[i], police_station_name_list[i]))

        self.fields['police_station'] = forms.ChoiceField(choices=POLICE_STATION_CHOICES)