from django.urls import path

from . import views

urlpatterns = [
    # path('<int:pk>/details/', views.client_detail, name='client_detail'),
    path('<int:pk>/edit-team/', views.edit_team, name='edit_team'),
    # path('<int:pk>/delete/', views.delete_client, name='delete_client'),
    # path('client/', views.client_list, name='client_list'),
    # path('add_client/', views.add_client, name='add_client'),
]