from django.urls import path

from . import views

app_name ='leads'

urlpatterns = [
    path('lead_list/', views.LeadListView.as_view(), name='list'),
    path('add_lead/', views.LeadCreateView.as_view(), name='add'),
    path('lead_detail/<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('delete_lead/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    path('edit_lead/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    path('<int:pk>/convert/', views.ConvertToClientView.as_view(), name='convert_to'),


]