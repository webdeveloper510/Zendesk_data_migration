from django.urls import path
from .import views

urlpatterns = [
    # path('showuserss', views.ShowTicket.as_view()),
    # path('attach_file', views.attachFile.as_view()),
    # path("attachment_ticket", views.Create_ticket_with_attachment),
    path('save_customer_ticket_excel', views.save_customer_ticket_excel),
    path('customer_data', views.CustomerData.as_view()),
    path('customer_create', views.CustomerCreate.as_view()),
    path('delete',views.deleteuser),
    path('save_user', views.save_customer_data),
    path('showuser_requster', views.ShowUser.as_view()),
    
    ########### For Yokohama ################
    path("customerdata", views.Addcustomer.as_view()),
    path("addticket", views.AddTicket.as_view()),
    path('save_csv', views.save_csv_data),
    path('request_uid',views.requester_id),
    path("sizemap", views.Sizemapping),
    path('designmap', views.Designmapping),
    path('li_si_prmap',views.LI_SImapping),
    path('defect_code',views.defect_code_mapping),
    path('show_yoko_ticket', views.ShowYokoTicket),
    path('fake_user',views.fake_user)

]