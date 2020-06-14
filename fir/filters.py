import django_filters

from . import models


class FirFilterAll(django_filters.FilterSet):
    class Meta:
        model = models.FIR
        fields = {
            'sub_division': ['exact'],
            'police_station': ['exact'],
            'fir_no': ['exact'],
            'date_created': ['lte', 'gte'],
            'io_name': ['contains'],
            'accused_name': ['contains'],
            'under_section': ['contains'],
            'accused_status': ['exact'],
            'limitation_period': ['lte', 'gte'],
            'current_status': ['exact'],
            'put_in_ssp_office': ['exact'],
            'put_in_ssp_office_date': ['lte', 'gte'],
            'ssp_approved': ['exact'],
            'put_in_court': ['exact'],
            'put_in_court_date': ['lte', 'gte'],
            'received_in_court': ['exact'],
            'received_in_court_date': ['lte', 'gte'],
            'court_status': ['exact'],
            'reverted_by_court_date': ['lte', 'gte'],
            'received_from_court_date': ['lte', 'gte'],
            'appointed_io': ['contains'],
            'is_closed' : ['exact'],
        }

class FirFilterSubDivision(django_filters.FilterSet):
    class Meta:
        model = models.FIR
        fields = {
            'police_station': ['exact'],
            'fir_no': ['exact'],
            'date_created': ['lte', 'gte'],
            'io_name': ['contains'],
            'accused_name': ['contains'],
            'under_section': ['contains'],
            'accused_status': ['exact'],
            'limitation_period': ['lte', 'gte'],
            'current_status': ['exact'],
            'put_in_ssp_office': ['exact'],
            'put_in_ssp_office_date': ['lte', 'gte'],
            'ssp_approved': ['exact'],
            'put_in_court': ['exact'],
            'put_in_court_date': ['lte', 'gte'],
            'received_in_court': ['exact'],
            'received_in_court_date': ['lte', 'gte'],
            'court_status': ['exact'],
            'reverted_by_court_date': ['lte', 'gte'],
            'received_from_court_date': ['lte', 'gte'],
            'appointed_io': ['contains'],
            'is_closed' : ['exact'],
        }

class FirFilterPoliceStationCourt(django_filters.FilterSet):
    class Meta:
        model = models.FIR
        fields = {
            'fir_no': ['exact'],
            'date_created': ['lte', 'gte'],
            'io_name': ['contains'],
            'accused_name': ['contains'],
            'under_section': ['contains'],
            'accused_status': ['exact'],
            'limitation_period': ['lte', 'gte'],
            'current_status': ['exact'],
            'put_in_ssp_office': ['exact'],
            'put_in_ssp_office_date': ['lte', 'gte'],
            'ssp_approved': ['exact'],
            'put_in_court': ['exact'],
            'put_in_court_date': ['lte', 'gte'],
            'received_in_court': ['exact'],
            'received_in_court_date': ['lte', 'gte'],
            'court_status': ['exact'],
            'reverted_by_court_date': ['lte', 'gte'],
            'received_from_court_date': ['lte', 'gte'],
            'appointed_io': ['contains'],
            'is_closed' : ['exact'],
        }
        