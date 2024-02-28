from django.urls import path
from .import views

urlpatterns = [
    path('user_create', views.UserCreate),
    path('bulk_ticket', views.Create_ticket),
    path('showuser', views.ShowTicket.as_view()),
    path('attach_file', views.attachFile.as_view()),
    path("attachment_ticket", views.Create_ticket_with_attachment),
    path('insert_excel', views.save_excel_data),
    # path("user_del", views.data_del),
    path('customer_data', views.CustomerData.as_view()),
    path('delete',views.deleteuser)
]
