from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from .models import Lead
from .forms import AddLeadForm




@login_required
def delete_lead(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead_name = lead.first_name
    lead.delete()

    # messages.add_message(request, messages.INFO, "the lead was deleted")
    # messages.success(request,  "{lead_name} Profile  details updated.")
    messages.success(request, f"{lead_name} has been deleted.")

    return redirect('leads_list')

@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    # lead=Lead.objects.filter(created_by=request.user).get(pk=pk)

    return render(request, 'lead/leads_detail.html', {
        'lead':lead
    })

@login_required
def leads_list(request):
    # leads = Lead.objects.filter(created_by=request.user, convert_to_client = False)
    leads = Lead.objects.filter(created_by=request.user)


    return render(request, 'lead/leads_list.html', {
        'leads': leads
    })

@login_required
def edit_lead(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            messages.success(request, f"{lead.first_name} has been edited successfully.")
            return redirect('leads_list')
    else:
        
        form = AddLeadForm(instance=lead)

        return render(request, 'lead/edit_lead.html', {
            'form':form
        })


@login_required
def add_lead(request):
    if request.method == 'POST':
        form = AddLeadForm(request.POST)

        if form.is_valid():
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.save()
            
            messages.success(request, f"{lead.first_name} has been added successfully.")

            return redirect('leads_list')  # Redirect to a success page or another relevant page
    else:
        form = AddLeadForm()

    return render(request, 'lead/add_lead.html', {
        'form': form
    })
