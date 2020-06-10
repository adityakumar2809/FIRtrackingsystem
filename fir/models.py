from django.db import models

# Create your models here.


class FIR(models.Model):

    PHASE_CHOICES=[(1,1),(2,2),(3,3)]
    ACCUSED_STATUS_CHOICES = [('arrested','Arrested'),('not_arrested','Not Arrested'),('po','PO')]
    CURRENT_STATUS_CHOICES = [('under_investigation','Under Investigation'),('challan_filed','Challan Filed'),('untraced','Untraced'),('cancelled','Cancelled')]
    COURT_STATUS_CHOICES = [('pending','Pending'),('accepted','Accepted'),('reinvestigation','Reinvestigation')]

    sub_division = models.ForeignKey("location.SubDivision", related_name='firs', on_delete=models.CASCADE)
    police_station = models.ForeignKey("location.PoliceStation", related_name='firs', on_delete=models.CASCADE)

    fir_no = models.CharField(max_length=50)
    phase = models.PositiveIntegerField(choices=PHASE_CHOICES)
    date_created = models.DateField(auto_now=True)

    io_name = models.CharField(max_length=50, blank=True, null=True)
    accused_name = models.TextField(blank=True, null=True)
    under_section = models.CharField(max_length=50, blank=True, null=True)
    accused_status = models.CharField(max_length=50, choices=ACCUSED_STATUS_CHOICES, blank=True, null=True)
    limitation_period = models.PositiveIntegerField(blank=True, null=True)
    
    current_status = models.CharField(max_length=50, choices=CURRENT_STATUS_CHOICES, blank=True, null=True)
    put_in_ssp_office = models.BooleanField(default=False)
    put_in_ssp_office_date = models.DateField(blank=True, null=True)
    ssp_approved = models.BooleanField(default=False)

    put_in_court = models.BooleanField(default=False)
    put_in_court_date = models.DateField(blank=True, null=True)

    received_in_court = models.BooleanField(default=False)
    received_in_court_date = models.DateField(blank=True, null=True)
    court_status = models.CharField(max_length=50, choices=COURT_STATUS_CHOICES, blank=True,  null=True)
    reverted_by_court_date = models.DateField(blank=True,  null=True)

    received_from_court_date = models.DateField(blank=True,  null=True)
    appointed_io = models.CharField(max_length=50, blank=True,  null=True)


    def __str__(self):
        return f'{self.sub_division} - {self.police_station} - {self.fir_no} - {self.phase}'

    class Meta():
        unique_together = ['sub_division', 'police_station', 'fir_no', 'phase']
        ordering = ['sub_division', 'police_station', '-fir_no', 'phase']
        verbose_name = 'FIR'
        verbose_name_plural = 'FIRs'   
