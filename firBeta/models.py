from django.db import models

# Create your models here.


class FIR(models.Model):

    sub_division = models.ForeignKey(
        "location.SubDivision", related_name='fir_list', on_delete=models.CASCADE)
    police_station = models.ForeignKey(
        "location.PoliceStation", related_name='fir_list', on_delete=models.CASCADE)

    fir_no = models.CharField(max_length=50)

    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sub_division} - {self.police_station} - {self.fir_no}'

    class Meta():
        unique_together = ['sub_division', 'police_station', 'fir_no']
        ordering = ['sub_division', 'police_station', '-pk']
        verbose_name = 'FIR'
        verbose_name_plural = 'FIRs'


class FIRPhase(models.Model):

    PHASE_CHOICES = [(1, 1), (2, 2), (3, 3)]
    CURRENT_STATUS_CHOICES = [('Under Investigation','Under Investigation'),('Challan Filed','Challan Filed'),('Untraced','Untraced'),('Cancelled','Cancelled')]
    VRK_STATUS_CHOICES = [('Pending', 'Pending'),('Approved', 'Approved')]
    NC_STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Reinvestigation', 'Reinvestigation')]

    fir = models.ForeignKey(
        "firBeta.FIR", related_name='phases', on_delete=models.CASCADE)
    phase_index = models.IntegerField(choices=PHASE_CHOICES)
    date_registered = models.DateField()
    date_created_on_system = models.DateField(auto_now_add=True)

    under_section = models.CharField(max_length=100)
    io_name = models.CharField(max_length=100)
    accused_name = models.TextField(blank=True, null=True)
    accused_status = models.TextField(blank=True, null=True)
    limitation_period = models.PositiveIntegerField()

    current_status = models.CharField(max_length=50, choices=CURRENT_STATUS_CHOICES)
    current_status_date = models.DateField(blank=True, null=True)

    vrk_receival_date = models.DateField(blank=True, null=True)
    vrk_status = models.CharField(max_length=50, choices=VRK_STATUS_CHOICES, blank=True, null=True)
    vrk_status_date = models.DateField(blank=True, null=True)
    vrk_sent_back_date = models.DateField(blank=True, null=True)

    received_from_vrk_date = models.DateField(blank=True, null=True)
    put_in_court_date = models.DateField(blank=True, null=True)

    nc_receival_date = models.DateField(blank=True, null=True)
    nc_status = models.CharField(max_length=50, choices=NC_STATUS_CHOICES, blank=True, null=True)
    nc_status_date = models.DateField(blank=True, null=True)
    nc_sent_back_date = models.DateField(blank=True, null=True)

    received_from_nc_date = models.DateField(blank=True, null=True)
    appointed_io = models.CharField(max_length=100, blank=True, null=True)
    appointed_io_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.fir.sub_division} - {self.fir.police_station} - {self.fir.fir_no} - {self.phase_index}'

    class Meta():
        unique_together = ['fir', 'phase_index']
        ordering = ['-fir__pk', 'phase_index']
        verbose_name = 'FIR Phase'
        verbose_name_plural = 'FIR Phases'


class LastMailDate(models.Model):
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.date}'