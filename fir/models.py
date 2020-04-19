from django.db import models

# Create your models here.


class FIR(models.Model):

    PHASE_CHOICES=[(1,1),(2,2),(3,3)]
    ACCUSED_STATUS_CHOICES = [('arrested','Arrested'),('not_arrested','Not Arrested'),('po','PO')]
    CURRENT_STATUS_CHOICES = [('under_invertigation','Under Invertigation'),('challan_filed','Challan Filed'),('untraced','Untraced'),('cancelled','Cancelled')]
    COURT_STATUS_CHOICES = [('pending','Pending'),('accepted','Accepted'),('reinvestigation','Reinvestigation')]

    sub_division = models.ForeignKey("location.SubDivision", related_name='firs', on_delete=models.CASCADE)
    police_station = models.ForeignKey("location.PoliceStation", related_name='firs', on_delete=models.CASCADE)

    fir_no = models.CharField(max_length=50)
    phase = models.PositiveIntegerField(choices=PHASE_CHOICES)
    date_created = models.DateField(auto_now=True)

    io_name = models.CharField(max_length=50)
    accused_name = models.TextField()
    accused_status = models.CharField(max_length=50, choices=ACCUSED_STATUS_CHOICES)
    limitation_period = models.PositiveIntegerField()
    
    current_status = models.CharField(max_length=50, choices=CURRENT_STATUS_CHOICES)
    ssp_approved = models.BooleanField(default=False)
    put_in_court = models.BooleanField(default=False)
    put_in_court_date = models.DateField()

    received_in_court = models.BooleanField(default=False)
    received_in_court_date = models.DateField()
    court_status = models.CharField(max_length=50, choices=COURT_STATUS_CHOICES)
    reverted_by_court_date = models.DateField()

    received_from_court_date = models.DateField()
    appointed_io = models.CharField(max_length=50)


    def __str__(self):
        return f'{self.sub_division} - {self.police_station} - {self.fir_no} - {self.phase}'

    class Meta():
        unique_together = ['sub_division', 'police_station', 'fir_no', 'phase']
        ordering = ['-fir_no','phase']
        verbose_name = 'FIR'
        verbose_name_plural = 'FIRs'   
