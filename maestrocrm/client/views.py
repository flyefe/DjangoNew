from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Client
from .forms import AddClientForm
from lead.models import Lead


@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            
            messages.success(request, f"{client.first_name} has been added successfully.")

            return redirect('client_list')  # Redirect to a success page or another relevant page
    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form': form
    })


@login_required
def convert_to_client(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    client = Client.objects.create(
        first_name=lead.first_name,
        status='open',  # default to 'open'
        open_date=timezone.now(),
        assigned_to=request.user,
        traffic_source=lead.traffic_source if hasattr(lead, 'traffic_source') else '',
        converted_by=request.user,
        converted_at=timezone.now()
    )

    lead.convert_to_client = True
    lead.save()
    messages.success(request, f"{lead.first_name} has been converted to a Client!")
    return redirect('client_list')

@login_required
def client_list(request):
    clients = Client.objects.filter(converted_by=request.user)

    return render(request, 'client/client_list.html', {
        'clients': clients
    })
