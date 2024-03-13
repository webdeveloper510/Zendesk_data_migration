from django.urls import path
from .import views

urlpatterns = [
    path('user_create', views.UserCreate),
    path('bulk_ticket', views.Create_ticket),
    path('showuserss', views.ShowTicket.as_view()),
    path('attach_file', views.attachFile.as_view()),
    path("attachment_ticket", views.Create_ticket_with_attachment),
    path('insert_excel', views.save_excel_data),
    # path("user_del", views.test),
    path('customer_data', views.CustomerData.as_view()),
    path('customer_create', views.CustomerCreate.as_view()),
    path('delete',views.deleteuser),
    path('save_user', views.save_customer_data),
    path("customerdata", views.Addcustomer.as_view()),
    path('showuser', views.ShowUser.as_view()),
    path('save_csv', views.save_csv_data)

]
