from django.db import models

# Create your models here.
# class Customer(models.Model):
#     job_type = models.CharField(max_length=200)
#     url = models.CharField(max_length=300)
#     status = models.CharField(max_length=100)
#     complete_json = models.CharField(max_length=500)



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



class UserData(models.Model):
    email = models.CharField(max_length=200,null=True, blank=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    region = models.CharField(max_length=500,null=True, blank=True)
    account_group = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)

    customer = models.CharField(max_length=500,null=True, blank=True)
    country = models.CharField(max_length=500,null=True, blank=True)
    search_term = models.CharField(max_length=500,null=True, blank=True)

    street = models.CharField(max_length=500,null=True, blank=True)
    house_number  = models.CharField(max_length=200,null=True, blank=True)
    street_2 = models.CharField(max_length=500,null=True, blank=True)
    street_3  = models.CharField(max_length=200,null=True, blank=True)
    street_4 = models.CharField(max_length=500,null=True, blank=True)
    street_5 = models.CharField(max_length=500,null=True, blank=True)
    city = models.CharField(max_length=500,null=True, blank=True)
    postal_code = models.CharField(max_length=500,null=True, blank=True)
    country = models.CharField(max_length=500,null=True, blank=True)
    branch  = models.CharField(max_length=200,null=True, blank=True)
    
class UserResponse(models.Model):
    job_type = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    status = models.CharField(max_length=100)
    complete_json = models.CharField(max_length=500)  


class UserMapping(models.Model):
    user_ids = models.CharField(max_length=200,null=True, blank=True)
    customer_number = models.CharField(max_length=200,null=True, blank=True)


class ExcelSize(models.Model):
    map_value = models.CharField(max_length=200,null=True, blank=True)
    size_value = models.CharField(max_length=200,null=True, blank=True)


class CustomerTicket(models.Model):
    unique_id = models.CharField(max_length=300,null=True, blank=True)
    date = models.CharField(max_length=300,null=True, blank=True)
    no_of_tyre = models.CharField(max_length=300,null=True, blank=True)
    size = models.CharField(max_length=300,null=True, blank=True)
    design = models.CharField(max_length=300,null=True, blank=True)
    li_si_pr = models.CharField(max_length=300,null=True, blank=True)
    type = models.CharField(max_length=300,null=True, blank=True)
    cat_no = models.CharField(max_length=300,null=True, blank=True)
    tyre_serial_no = models.CharField(max_length=300,null=True, blank=True)
    plant = models.CharField(max_length=300,null=True, blank=True)
    claim_no = models.CharField(max_length=300,null=True, blank=True)
    date_of_invoice = models.CharField(max_length=300,null=True, blank=True)
    invoice_details = models.CharField(max_length=300,null=True, blank=True)
    remaining_tread_depth = models.CharField(max_length=300,null=True, blank=True)
    defect_code_description = models.CharField(max_length=300,null=True, blank=True)
    our_recommendation = models.CharField(max_length=300,null=True, blank=True)
    remarks = models.CharField(max_length=300,null=True, blank=True)
    disposed_by = models.CharField(max_length=300,null=True, blank=True)
    customer_code = models.CharField(max_length=300,null=True, blank=True)
    customer_code_update = models.CharField(max_length=300,null=True, blank=True)
    customer_name = models.CharField(max_length=300,null=True, blank=True)
    country_working = models.CharField(max_length=300,null=True, blank=True)
    region = models.CharField(max_length=300,null=True, blank=True)
    requester_id = models.CharField(max_length=300,null=True, blank=True)
    mapsize = models.CharField(max_length=300,null=True, blank=True)
    map_li_si_pr = models.CharField(max_length=5000,null=True, blank=True)
    map_design = models.CharField(max_length=300,null=True, blank=True)
    map_defect_code = models.CharField(max_length=300,null=True, blank=True)


    # user_mapping = models.ForeignKey(UserMapping, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_tickets')
    
    # excel_size = models.ForeignKey(ExcelSize, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_tickets')



class DesignLISIMAP(models.Model):
    mapdesign = models.CharField(max_length=300,null=True, blank=True)
    excel_design = models.CharField(max_length=300,null=True, blank=True)
    



class LI_SI_PRMAP(models.Model):
    map_li_si_pr = models.CharField(max_length=300,null=True, blank=True)
    excel_li_si = models.CharField(max_length=300,null=True, blank=True)


class Defect_code(models.Model):
    map_defect_code = models.CharField(max_length=300,null=True, blank=True)
    excel_defect_code = models.CharField(max_length=300,null=True, blank=True)



#for testing
class Fakeuser(models.Model):
    name = models.CharField(max_length=300,null=True, blank=True)
    email = models.CharField(max_length=300,null=True, blank=True)


#for ticket ids
class Ticket_ids(models.Model):
    ticket_ids = models.CharField(max_length=300,null=True, blank=True)
    claims = models.CharField(max_length=300,null=True, blank=True)