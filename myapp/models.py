from django.db import models

# Create your models here.
class Tickets(models.Model):
    job_type = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    status = models.CharField(max_length=100)
    complete_json = models.CharField(max_length=500)
    # def __str__(self):
    #     return self.url


class Plant(models.Model):
    date = models.CharField(max_length=200,null=True, blank=True)
    number_of_tyres = models.CharField(max_length=500,null=True, blank=True)
    size = models.CharField(max_length=200,null=True, blank=True)
    design = models.CharField(max_length=500,null=True, blank=True)
    LI_SI_PR = models.CharField(max_length=500,null=True, blank=True)
    type = models.CharField(max_length=200,null=True, blank=True)
    cat_no = models.CharField(max_length=200,null=True, blank=True)
    tyre_serial_number = models.CharField(max_length=200,null=True, blank=True)
    plant = models.CharField(max_length=500,null=True, blank=True)
    claim_no = models.CharField(max_length=200,null=True, blank=True)
    date_of_mounting = models.CharField(max_length=200,null=True, blank=True)
    invoice_details = models.CharField(max_length=500,null=True, blank=True)
    remaining_tread_depth = models.CharField(max_length=200,null=True, blank=True)
    defect = models.CharField(max_length=500,null=True, blank=True)
    our_recommendation = models.CharField(max_length=200,null=True, blank=True)
    remarks = models.CharField(max_length=500,null=True, blank=True)
    dispose_by = models.CharField(max_length=500,null=True, blank=True)
    customer_name = models.CharField(max_length=500,null=True, blank=True)
    country = models.CharField(max_length=200,null=True, blank=True)
    customer_ref_no = models.CharField(max_length=500,null=True, blank=True)
    ND_Used = models.CharField(max_length=200,null=True, blank=True)
    old_ticket_no = models.CharField(max_length=200,null=True, blank=True)



