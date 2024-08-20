from django.urls import path
from .import views
from .import db_mapping

urlpatterns = [
   
    ########### Add claim and user in db ###################
    path('save_customer_ticket_excel', views.save_customer_ticket_excel),
    path('save_user', views.save_customer_data),

    ########### Add customer code ################
    path('add_customer_code', views.AddUserCustomerCode.as_view()),
    
    ########### Add Customer API for Yokohama ################
    path("customerdata", views.Addcustomer.as_view()),

    ########### Add ticket API  ################
    path("addticket", views.AddTicket.as_view()),

    ############ Mapping functions #############
    path('save_mapping_data', views.save_mapping_data),
    path('request_uid',views.requester_id),
    path("sizemap", views.Sizemapping),
    path('designmap', views.Designmapping),
    path('li_si_prmap',views.LI_SImapping),
    path('defect_code',views.defect_code_mapping),
    path('save_claim_ids', views.ShowYokoTicket),

]