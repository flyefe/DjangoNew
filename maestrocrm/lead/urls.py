from django.urls import path

from . import views

urlpatterns = [
    path('leads_list', views.leads_list, name='leads_list'),
    path('add_lead/', views.add_lead, name='add_lead'),
    path('leads_detail/<int:pk>/', views.leads_detail, name='leads_detail'),
    path('delete_lead/<int:pk>/delete/', views.delete_lead, name='delete_lead'),
    path('etdit_lead/<int:pk>/edit/', views.edit_lead, name='edit_lead'),

]