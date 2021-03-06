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


class FIRFilterPSForm(forms.Form):

    FIR_CLOSED_CHOICES = [(None,'Any'),(True,'Yes'),(False,'No')]

    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('0-180', 'Upto 6 months'), ('0-365', 'Upto 1 year'), ('0-730', 'Upto 2 years'), ('0-1825','Upto 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('0-5', 'In next 5 days'), ('0-10', 'In next 10 days'), ('0-20', 'In next 20 days'), ('0-30', 'In next 1 month'), ('31-inf', 'More than 1 month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    GAP_PS_SENT_NC_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('6-inf','More than 5 days'), ('11-inf','More than 10 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months')]
    VRK_BEFORE_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days')]
    VRK_AFTER_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    NC_APPROVED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    CHALLAN_FILED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_CLOSED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')] 
    FIR_REGISTERED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')] 
    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_ps_sent_nc_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_NC_RECEIVED_CHOICES)
    gap_nc_marked_reinvestigation_nc_sent = forms.ChoiceField(required=False, choices=GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_before_approval_pendency = forms.ChoiceField(required=False, choices=VRK_BEFORE_APPROVAL_PENDENCY_CHOICES)
    vrk_after_approval_pendency = forms.ChoiceField(required=False, choices=VRK_AFTER_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)
    nc_approved_time_period = forms.ChoiceField(required=False, choices=NC_APPROVED_TIME_PERIOD_CHOICES)
    marked_reinvestigation_time_period = forms.ChoiceField(required=False, choices=MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES)
    challan_filed_time_period = forms.ChoiceField(required=False, choices=CHALLAN_FILED_TIME_PERIOD_CHOICES)
    fir_closed_time_period = forms.ChoiceField(required=False, choices=FIR_CLOSED_TIME_PERIOD_CHOICES)
    fir_registered_time_period = forms.ChoiceField(required=False, choices=FIR_REGISTERED_TIME_PERIOD_CHOICES)

    is_closed = forms.ChoiceField(required=False, choices=FIR_CLOSED_CHOICES)


class FIRFilterVRKForm(forms.Form):

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

    FIR_CLOSED_CHOICES = [(None,'Any'),(True,'Yes'),(False,'No')]
    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('0-180', 'Upto 6 months'), ('0-365', 'Upto 1 year'), ('0-730', 'Upto 2 years'), ('0-1825','Upto 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('0-5', 'In next 5 days'), ('0-10', 'In next 10 days'), ('0-20', 'In next 20 days'), ('0-30', 'In next 1 month'), ('31-inf', 'More than 1 month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    GAP_PS_SENT_NC_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('6-inf','More than 5 days'), ('11-inf','More than 10 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months')]
    VRK_BEFORE_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days')]
    VRK_AFTER_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    NC_APPROVED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    CHALLAN_FILED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_CLOSED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_REGISTERED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]

    sub_division = forms.ChoiceField(required=False, choices=SUB_DIVISION_CHOICES)
    police_station = forms.ChoiceField(required=False, choices=POLICE_STATION_CHOICES)

    # expiry_date_lower_limit = forms.CharField(required=False)
    # expiry_date_upper_limit = forms.CharField(required=False)

    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_ps_sent_nc_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_NC_RECEIVED_CHOICES)
    gap_nc_marked_reinvestigation_nc_sent = forms.ChoiceField(required=False, choices=GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_before_approval_pendency = forms.ChoiceField(required=False, choices=VRK_BEFORE_APPROVAL_PENDENCY_CHOICES)
    vrk_after_approval_pendency = forms.ChoiceField(required=False, choices=VRK_AFTER_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)
    nc_approved_time_period = forms.ChoiceField(required=False, choices=NC_APPROVED_TIME_PERIOD_CHOICES)
    marked_reinvestigation_time_period = forms.ChoiceField(required=False, choices=MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES)
    challan_filed_time_period = forms.ChoiceField(required=False, choices=CHALLAN_FILED_TIME_PERIOD_CHOICES)
    fir_closed_time_period = forms.ChoiceField(required=False, choices=FIR_CLOSED_TIME_PERIOD_CHOICES)
    fir_registered_time_period = forms.ChoiceField(required=False, choices=FIR_REGISTERED_TIME_PERIOD_CHOICES)

    is_closed = forms.ChoiceField(required=False, choices=FIR_CLOSED_CHOICES)


class FIRFilterNCForm(forms.Form):

    FIR_CLOSED_CHOICES = [(None,'Any'),(True,'Yes'),(False,'No')]

    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('0-180', 'Upto 6 months'), ('0-365', 'Upto 1 year'), ('0-730', 'Upto 2 years'), ('0-1825','Upto 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('0-5', 'In next 5 days'), ('0-10', 'In next 10 days'), ('0-20', 'In next 20 days'), ('0-30', 'In next 1 month'), ('31-inf', 'More than 1 month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    GAP_PS_SENT_NC_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('6-inf','More than 5 days'), ('11-inf','More than 10 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months')]
    VRK_BEFORE_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days')]
    VRK_AFTER_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    NC_APPROVED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    CHALLAN_FILED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_CLOSED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_REGISTERED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]

    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_ps_sent_nc_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_NC_RECEIVED_CHOICES)
    gap_nc_marked_reinvestigation_nc_sent = forms.ChoiceField(required=False, choices=GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_before_approval_pendency = forms.ChoiceField(required=False, choices=VRK_BEFORE_APPROVAL_PENDENCY_CHOICES)
    vrk_after_approval_pendency = forms.ChoiceField(required=False, choices=VRK_AFTER_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)
    nc_approved_time_period = forms.ChoiceField(required=False, choices=NC_APPROVED_TIME_PERIOD_CHOICES)
    marked_reinvestigation_time_period = forms.ChoiceField(required=False, choices=MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES)
    challan_filed_time_period = forms.ChoiceField(required=False, choices=CHALLAN_FILED_TIME_PERIOD_CHOICES)
    fir_closed_time_period = forms.ChoiceField(required=False, choices=FIR_CLOSED_TIME_PERIOD_CHOICES)
    fir_registered_time_period = forms.ChoiceField(required=False, choices=FIR_REGISTERED_TIME_PERIOD_CHOICES)

    is_closed = forms.ChoiceField(required=False, choices=FIR_CLOSED_CHOICES)


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

    FIR_CLOSED_CHOICES = [(None,'Any'),(True,'Yes'),(False,'No')]
    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('0-180', 'Upto 6 months'), ('0-365', 'Upto 1 year'), ('0-730', 'Upto 2 years'), ('0-1825','Upto 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('0-5', 'In next 5 days'), ('0-10', 'In next 10 days'), ('0-20', 'In next 20 days'), ('0-30', 'In next 1 month'), ('31-inf', 'More than 1 month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    GAP_PS_SENT_NC_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('6-inf','More than 5 days'), ('11-inf','More than 10 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months')]
    VRK_BEFORE_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days')]
    VRK_AFTER_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    NC_APPROVED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    CHALLAN_FILED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_CLOSED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_REGISTERED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]

    sub_division = forms.ChoiceField(required=False, choices=SUB_DIVISION_CHOICES)
    police_station = forms.ChoiceField(required=False, choices=POLICE_STATION_CHOICES)

    # expiry_date_lower_limit = forms.CharField(required=False)
    # expiry_date_upper_limit = forms.CharField(required=False)

    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_ps_sent_nc_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_NC_RECEIVED_CHOICES)
    gap_nc_marked_reinvestigation_nc_sent = forms.ChoiceField(required=False, choices=GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_before_approval_pendency = forms.ChoiceField(required=False, choices=VRK_BEFORE_APPROVAL_PENDENCY_CHOICES)
    vrk_after_approval_pendency = forms.ChoiceField(required=False, choices=VRK_AFTER_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)
    nc_approved_time_period = forms.ChoiceField(required=False, choices=NC_APPROVED_TIME_PERIOD_CHOICES)
    marked_reinvestigation_time_period = forms.ChoiceField(required=False, choices=MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES)
    challan_filed_time_period = forms.ChoiceField(required=False, choices=CHALLAN_FILED_TIME_PERIOD_CHOICES)
    fir_closed_time_period = forms.ChoiceField(required=False, choices=FIR_CLOSED_TIME_PERIOD_CHOICES)
    fir_registered_time_period = forms.ChoiceField(required=False, choices=FIR_REGISTERED_TIME_PERIOD_CHOICES)

    is_closed = forms.ChoiceField(required=False, choices=FIR_CLOSED_CHOICES)


class FIRFilterDSPForm(forms.Form):

    POLICE_STATION_CHOICES = [(None,'---Select---')]

    FIR_CLOSED_CHOICES = [(None,'Any'),(True,'Yes'),(False,'No')]

    FIR_PENDENCY_CHOICES = [(None, '---Select---'), ('0-90','Upto 3 months'), ('0-180', 'Upto 6 months'), ('0-365', 'Upto 1 year'), ('0-730', 'Upto 2 years'), ('0-1825','Upto 5 years'), ('1825-inf', 'More than 5 years')]
    EXPIRY_DATE_CHOICES = [(None, '---Select---'), ('overdue-0', 'Overdue'), ('0-5', 'In next 5 days'), ('0-10', 'In next 10 days'), ('0-20', 'In next 20 days'), ('0-30', 'In next 1 month'), ('31-inf', 'More than 1 month')]
    GAP_PS_SENT_VRK_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_VRK_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_PS_RECEIVED_NC_SENT_CHOICES = [(None, '---Select---'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    GAP_PS_SENT_NC_RECEIVED_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    GAP_NC_SENT_PS_RECEIVED_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days')]
    GAP_PS_RECEIVED_MARK_IO_CHOICES = [(None, '---Select---'), ('6-inf','More than 5 days'), ('11-inf','More than 10 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months')]
    VRK_BEFORE_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days')]
    VRK_AFTER_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('4-inf','More than 3 days')]
    NC_APPROVAL_PENDENCY_CHOICES = [(None, '---Select---'), ('8-inf','More than 7 days'), ('16-inf','More than 15 days'), ('31-inf','More than 30 days'), ('61-inf','More than 2 months'), ('91-inf','More than 3 months'), ('181-inf','More than 6 months'), ('366-inf','More than 1 year')]
    NC_APPROVED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    CHALLAN_FILED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_CLOSED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]
    FIR_REGISTERED_TIME_PERIOD_CHOICES = [(None, '---Select---'), ('0-7','Within last 7 days'), ('0-15','Within last 15 days'), ('0-30','Within last 1 month'), ('0-60','Within last 2 months'), ('0-90','Within last 3 months'), ('0-180','Within last 6 months'), ('0-365','Within last 1 year'), ('0-730', 'Within last 2 years'), ('0-1825','Within last 5 years')]


    police_station = forms.ChoiceField(required=False, choices=POLICE_STATION_CHOICES)

    fir_no = forms.CharField(required=False)
    under_section = forms.CharField(required=False)
    
    gap_ps_sent_vrk_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_VRK_RECEIVED_CHOICES)
    gap_vrk_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_VRK_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_nc_sent = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_NC_SENT_CHOICES)
    gap_ps_sent_nc_received = forms.ChoiceField(required=False, choices=GAP_PS_SENT_NC_RECEIVED_CHOICES)
    gap_nc_marked_reinvestigation_nc_sent = forms.ChoiceField(required=False, choices=GAP_NC_MARKED_REINVESTIGATION_NC_SENT_CHOICES)
    gap_nc_sent_ps_received = forms.ChoiceField(required=False, choices=GAP_NC_SENT_PS_RECEIVED_CHOICES)
    gap_ps_received_mark_io = forms.ChoiceField(required=False, choices=GAP_PS_RECEIVED_MARK_IO_CHOICES)

    fir_pendency = forms.ChoiceField(required=False, choices=FIR_PENDENCY_CHOICES)
    expiry_date = forms.ChoiceField(required=False, choices=EXPIRY_DATE_CHOICES)

    vrk_before_approval_pendency = forms.ChoiceField(required=False, choices=VRK_BEFORE_APPROVAL_PENDENCY_CHOICES)
    vrk_after_approval_pendency = forms.ChoiceField(required=False, choices=VRK_AFTER_APPROVAL_PENDENCY_CHOICES)
    nc_approval_pendency = forms.ChoiceField(required=False, choices=NC_APPROVAL_PENDENCY_CHOICES)
    nc_approved_time_period = forms.ChoiceField(required=False, choices=NC_APPROVED_TIME_PERIOD_CHOICES)
    marked_reinvestigation_time_period = forms.ChoiceField(required=False, choices=MARKED_REINVESTIGATION_TIME_PERIOD_CHOICES)
    challan_filed_time_period = forms.ChoiceField(required=False, choices=CHALLAN_FILED_TIME_PERIOD_CHOICES)
    fir_closed_time_period = forms.ChoiceField(required=False, choices=FIR_CLOSED_TIME_PERIOD_CHOICES)
    fir_registered_time_period = forms.ChoiceField(required=False, choices=FIR_REGISTERED_TIME_PERIOD_CHOICES)

    is_closed = forms.ChoiceField(required=False, choices=FIR_CLOSED_CHOICES)


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