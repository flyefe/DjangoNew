from django.urls import path

from . import views

app_name ='leads'

urlpatterns = [
    path('lead_list/', views.LeadListView.as_view(), name='list'),
    path('add_lead/', views.add_lead, name='add'),
    path('lead_detail/<int:pk>/', views.leads_detail, name='detail'),
    path('delete_lead/<int:pk>/delete/', views.delete_lead, name='delete'),
    path('edit_lead/<int:pk>/edit/', views.edit_lead, name='edit'),
    path('<int:pk>/convert/', views.convert_to_client, name='convert_to'),


]