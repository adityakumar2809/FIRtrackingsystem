from django import template
import datetime

from firBeta import models

register=template.Library()

@register.filter
def will_expire_at(pk):
    try:
        fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
        if fir_phase.fir.is_closed == True:
            return 3
        if fir_phase.phase_index == 1:
            time_diff = (datetime.date.today() - fir_phase.date_registered).days
        else:
            fir_prev_phase = models.FIRPhase.objects.get(fir__exact = fir_phase.fir, phase_index__exact = fir_phase.phase_index - 1)
            time_diff = (datetime.date.today() - fir_prev_phase.appointed_io_date).days
        if time_diff > fir_phase.limitation_period:
            return 0
        elif fir_phase.limitation_period - time_diff <= 10:
            return 1
        elif fir_phase.limitation_period - time_diff <= 20:
            return 2
        else:
            return 3
    except:
        return -1


@register.filter
def is_last_phase(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    fir_phase_list = fir_phase.fir.phases.all()
    if len(fir_phase_list) == fir_phase.phase_index:
        return True
    else:
        return False


@register.filter
def is_third_phase(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    fir_phase_list = fir_phase.fir.phases.all()
    if len(fir_phase_list) == 3:
        return True
    else:
        return False


@register.filter
def get_expiry_date(pk):
    try:
        fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
        if fir_phase.phase_index == 1:
            expiry_date = fir_phase.date_registered + datetime.timedelta(days = fir_phase.limitation_period)
        else:
            fir_prev_phase = models.FIRPhase.objects.get(fir__exact = fir_phase.fir, phase_index__exact = fir_phase.phase_index - 1)
            expiry_date = fir_prev_phase.appointed_io_date + datetime.timedelta(days = fir_phase.limitation_period) 
        return expiry_date
    except:
        return 0


@register.filter
def all_fields_filled(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    field_names = [f.name for f in models.FIRPhase._meta.get_fields()]

    for field_name in field_names:
        value = getattr(fir_phase, field_name)
        if value in [None, '']:
            return False
    
    return True


@register.filter
def get_color_shade(phase_index):
    return 4 if phase_index == 1 else 3 if phase_index == 2 else 2


@register.filter
def gap_greater_than_3(pk, stage):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    if stage == 'ps-sent-vrk-received':
        if (fir_phase.current_status in ['Untraced', 'Cancelled']) and (not fir_phase.vrk_receival_date):
            if (datetime.datetime.today().date() - fir_phase.current_status_date).days > 3:
                return True
    elif stage == 'vrk-sent-ps-received':
        if (fir_phase.vrk_sent_back_date) and (not fir_phase.received_from_vrk_date):
            if (datetime.datetime.today().date() - fir_phase.vrk_sent_back_date).days > 3:
                return True
    elif stage == 'ps-received-nc-sent':
        if (fir_phase.received_from_vrk_date) and (not fir_phase.put_in_court_date):
            if (datetime.datetime.today().date() - fir_phase.received_from_vrk_date).days > 30:
                return 'red'
            elif (datetime.datetime.today().date() - fir_phase.received_from_vrk_date).days > 15:
                return 'orange'
    elif stage == 'ps-sent-nc-received':
        if (fir_phase.put_in_court_date) and (not fir_phase.nc_receival_date):
            if (datetime.datetime.today().date() - fir_phase.put_in_court_date).days > 3:
                return True
    elif stage == 'nc-sent-ps-received':
        if (fir_phase.nc_sent_back_date) and (not fir_phase.received_from_nc_date):
            if (datetime.datetime.today().date() - fir_phase.nc_sent_back_date).days > 3:
                return True
    elif stage == 'ps-received_mark_io':
        if (fir_phase.received_from_nc_date) and (not fir_phase.appointed_io_date):
            if (datetime.datetime.today().date() - fir_phase.received_from_nc_date).days > 3:
                return True
    
    return False


@register.filter
def any_gap_greater_than_3(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    if (fir_phase.current_status in ['Untraced', 'Cancelled']) and (not fir_phase.vrk_receival_date):
        if (datetime.datetime.today().date() - fir_phase.current_status_date).days > 3:
            return True
    if (fir_phase.vrk_sent_back_date) and (not fir_phase.received_from_vrk_date):
        if (datetime.datetime.today().date() - fir_phase.vrk_sent_back_date).days > 3:
            return True
    if (fir_phase.received_from_vrk_date) and (not fir_phase.put_in_court_date):
        if (datetime.datetime.today().date() - fir_phase.received_from_vrk_date).days > 15:
            return True
    if (fir_phase.put_in_court_date) and (not fir_phase.nc_receival_date):
        if (datetime.datetime.today().date() - fir_phase.put_in_court_date).days > 3:
            return True
    if (fir_phase.nc_sent_back_date) and (not fir_phase.received_from_nc_date):
        if (datetime.datetime.today().date() - fir_phase.nc_sent_back_date).days > 3:
            return True
    if (fir_phase.received_from_nc_date) and (not fir_phase.appointed_io_date):
        if (datetime.datetime.today().date() - fir_phase.received_from_nc_date).days > 3:
            return True

    return False


@register.filter
def get_pendency_status(pk, stage):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    if stage == 'vrk-before-approval-pendency':
        if (fir_phase.vrk_receival_date) and (not fir_phase.vrk_sent_back_date) and (fir_phase.vrk_status != 'Approved'):
            if (datetime.datetime.today().date() - fir_phase.vrk_receival_date).days > 10:
                return 'red'
            elif (datetime.datetime.today().date() - fir_phase.vrk_receival_date).days > 5:
                return 'orange'
    elif stage == 'vrk-after-approval-pendency':
        if (fir_phase.vrk_receival_date) and (not fir_phase.vrk_sent_back_date) and (fir_phase.vrk_status == 'Approved'):
            if (datetime.datetime.today().date() - fir_phase.vrk_status_date).days > 10:
                return 'red'
            elif (datetime.datetime.today().date() - fir_phase.vrk_status_date).days > 5:
                return 'orange'
    
    return False

