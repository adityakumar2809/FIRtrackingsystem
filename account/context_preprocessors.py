from .import models

def UserList(request):
    police_station_record_keepers = [u['user'] for u in models.PoliceStationRecordKeeper.objects.all().values('user')]
    court_record_keepers = [u['user'] for u in models.CourtRecordKeeper.objects.all().values('user')]
    dsp_record_keepers = [u['user'] for u in models.DSPRecordKeeper.objects.all().values('user')]
    vrk_record_keepers = [u['user'] for u in models.VRKRecordKeeper.objects.all().values('user')]
    ssp_record_keepers = [u['user'] for u in models.SSPRecordKeeper.objects.all().values('user')]
    

    return {'police_station_record_keepers':police_station_record_keepers, 
            'court_record_keepers':court_record_keepers, 
            'dsp_record_keepers':dsp_record_keepers,
            'vrk_record_keepers':vrk_record_keepers,
            'ssp_record_keepers':ssp_record_keepers,
            }