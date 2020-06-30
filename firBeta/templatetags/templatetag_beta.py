from django import template
import datetime

from firBeta import models

register=template.Library()

@register.filter
def will_expire_at(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    time_diff = (datetime.date.today() - fir_phase.date_registered).days
    if time_diff > fir_phase.limitation_period:
        return 0
    elif fir_phase.limitation_period - time_diff <= 10:
        return 1
    elif fir_phase.limitation_period - time_diff <= 20:
        return 2
    else:
        return 3


@register.filter
def is_last_phase(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    fir_phase_list = fir_phase.fir.phases.all()
    if len(fir_phase_list) == fir_phase.phase_index:
        return True
    else:
        return False


@register.filter
def get_expiry_date(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    expiry_date = fir_phase.date_registered + datetime.timedelta(days = fir_phase.limitation_period) 
    return expiry_date


@register.filter
def all_fields_filled(pk):
    fir_phase = models.FIRPhase.objects.get(pk__exact=pk)
    field_names = [f.name for f in models.FIRPhase._meta.get_fields()]

    for field_name in field_names:
        value = getattr(fir_phase, field_name)
        if value in [None, '']:
            return False
    
    return True

