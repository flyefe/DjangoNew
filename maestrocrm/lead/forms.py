from django import forms
from .models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('first_name', 'email', 'description', 'priority', 'status',)
