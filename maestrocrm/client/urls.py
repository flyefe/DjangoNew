from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.convert_to_client, name='convert_to_client'),
    path('client/', views.client_list, name='client_list'),
]