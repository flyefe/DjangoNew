from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Client
from .forms import AddClientForm
from lead.models import Lead


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client_name = client.first_name
    client.delete()

    messages.success(request, f"{client.first_name} has been edited successfully.")
    return redirect(client_list)


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, f"{client.first_name} has been edited successfully.")
            return redirect('client_list')
    else:
        
        form = AddClientForm(instance=client)

        return render(request, 'client/edit_client.html', {
            'form':form
        })

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    # client=client.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'client/client_detail.html', {'client': client})



@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            messages.success(
                request, f"{client.first_name} has been added successfully.")

            return redirect(
                'client_list'
            )  # Redirect to a success page or another relevant page
    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {'form': form})



@login_required
def client_list(request):
    clients = Client.objects.filter()

    return render(request, 'client/client_list.html', {'clients': clients})

@login_required
def convert_to_lead(request, pk):
    lead = get_object_or_404(Client, created_by=request.user, pk=pk)
    lead = Lead.objects.create(
        first_name=client.first_name,
        status='open',  # default to 'open'
        open_date=timezone.now(),
        assigned_to=request.user,
        traffic_source=client.traffic_source
        if hasattr(client, 'traffic_source') else '',
        converted_by=request.user,
        converted_at=timezone.now(),
        created_by=request.user,)

    client.convert_to_client = True
    client.save()
    messages.success(request,
                     f"{client.first_name} has been converted to a Client! Update thier details.")
    return redirect('add_client')


@login_required
def convert_to_client(request, pk):
    client = get_object_or_404(Lead, created_by=request.user, pk=pk)
    client = Client.objects.create(
        first_name=client.first_name,
        status='open',  # default to 'open'
        open_date=timezone.now(),
        assigned_to=request.user,
        traffic_source=client.traffic_source
        if hasattr(client, 'traffic_source') else '',
        converted_by=request.user,
        converted_at=timezone.now(),
        created_by=request.user,)

    client.convert_to_client = True
    client.save()
    messages.success(request,
                     f"{client.first_name} has been converted to a Client! Update thier details.")
    return redirect('add_client')
