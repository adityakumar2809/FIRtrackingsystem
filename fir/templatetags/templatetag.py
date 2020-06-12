from django import template
import datetime

from fir import models

register=template.Library()


@register.filter
def is_last_phase(pk):
    fir_object = models.FIR.objects.get(pk__exact=pk)
    fir_phase = fir_object.phase
    fir_phase_list = models.FIR.objects.all().filter(fir_no__exact=fir_object.fir_no, police_station__exact=fir_object.police_station, sub_division__exact=fir_object.sub_division)

    if fir_phase==len(fir_phase_list):
        return True
    else:
        return False


@register.filter
def is_first_phase(pk):
    fir_object = models.FIR.objects.get(pk__exact=pk)
    fir_phase = fir_object.phase
    
    if fir_phase==1:
        return True
    else:
        return False


@register.filter
def is_next_phase_possible(pk):
    fir_object = models.FIR.objects.get(pk__exact=pk)
    fir_phase = fir_object.phase
    if fir_phase==3:
        return False
    fir_phase_list = models.FIR.objects.all().filter(fir_no__exact=fir_object.fir_no, police_station__exact=fir_object.police_station, sub_division__exact=fir_object.sub_division)

    if fir_phase==len(fir_phase_list):
        return True
    else:
        return False


@register.filter
def will_expire_at(pk):
    fir_object = models.FIR.objects.get(pk__exact=pk)
    time_diff = (datetime.date.today() - fir_object.date_created).days
    if time_diff > fir_object.limitation_period:
        return 0
    elif fir_object.limitation_period - time_diff <= 10:
        return 1
    elif fir_object.limitation_period - time_diff <= 20:
        return 2
    else:
        return 3