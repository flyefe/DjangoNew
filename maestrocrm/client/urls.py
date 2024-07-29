from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/convert/', views.convert_to_client, name='convert_to_client'),
    path('<int:pk>/details/', views.client_detail, name='client_detail'),
    path('<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('<int:pk>/delete/', views.delete_client, name='delete_client'),
    path('client/', views.client_list, name='client_list'),
    path('add_client/', views.add_client, name='add_client'),
]