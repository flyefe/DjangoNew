from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .models import Client
from lead.models import Lead
from lead.forms import AddLeadForm


@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    
    client=Client.objects.create(
        name=lead.name,
        email=lead.email,
        description=lead.description
    )
    
    lead.convert_to_client = True
    lead.save()
    messages.success(request, f"{lead.name} has ben converted to Customer!!!")
    return redirect('client_list')
        
@login_required
def client_list(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/client_list.html', {
        'clients': clients
    })