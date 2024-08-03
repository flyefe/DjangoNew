from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Client
from .forms import AddClientForm
from team.models import Team
# from lead.models import Lead


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client_name = client.first_name
    client.delete()

    messages.success(request, f"{client_name} has been deleted successfully.")
    return redirect('clients:list')


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(request, f"{client.first_name} has been edited successfully.")
            return redirect('clients:list')
    else:
        
        form = AddClientForm(instance=client)

        return render(request, 'client/edit_client.html', {
            'form': form
        })

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    # client=client.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'client/client_detail.html', {'client': client})



@login_required
def add_client(request):
    
    team=Team.objects.filter(created_by=request.user).first()

    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team=Team.objects.filter(created_by=request.user).first()

            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(
                request, f"{client.first_name} has been added successfully.")

            return redirect(
                'clients:list'
            )  # Redirect to a success page or another relevant page
    else:
        form = AddClientForm()

    return render(request, 'client/add_client.html', {
        'form': form,
        'team' : team
        })



@login_required
def client_list(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/client_list.html', {'clients': clients})