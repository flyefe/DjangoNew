from django import forms
from .models import Client

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name', 'middle_name', 'last_name', 'phone_number', 'email',
            'services', 'status', 'open_date', 'close_date', 'assigned_to',
            'traffic_source',
        ]
        # Remove readonly_fields if it's not needed
