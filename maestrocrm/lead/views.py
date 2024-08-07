from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy

from .models import Lead
from .forms import AddLeadForm

from django.contrib import messages
from django.utils import timezone
from client.models import Client
from team.models import Team



class LeadDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')
    success_message = "%(first_name)s has been deleted."

    def get_queryset(self):
        return Lead.objects.filter(created_by=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"{self.object.first_name} has been deleted."

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.get_success_message(None))
        return super().delete(request, *args, **kwargs)


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    # template_name = 'lead/lead_detail.html'
    # context_object_name = 'lead'
    # login_url = '/log-in/'  # Specify your custom login URL here if different

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Lead, created_by=self.request.user, pk=pk)


class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

    def get_queryset(self):      
        return  Lead.objects.filter(created_by=self.request.user, convert_to_client=False)



class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = AddLeadForm
    template_name = 'lead/edit_lead.html'
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        return Lead.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.object.first_name} has been edited successfully.")
        return response
    

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = AddLeadForm
    template_name = 'lead/add_lead.html'
    success_url = reverse_lazy('leads:list')

    def form_valid(self, form):
        # Get the team associated with the current user
        team = Team.objects.filter(created_by=self.request.user).first()
        
        # Assign the team and created_by fields to the lead instance
        lead = form.save(commit=False)
        lead.created_by = self.request.user
        lead.team = team
        lead.save()
        
        # Add a success message
        messages.success(self.request, f"{lead.first_name} has been added successfully.")
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(created_by=self.request.user).first()
        return context
    

class ConvertToClientView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = Team.objects.filter(created_by=request.user).first()

        client = Client.objects.create(
            first_name=lead.first_name,
            status='open',  # default to 'open'
            open_date=timezone.now(),
            assigned_to=request.user,
            traffic_source=lead.traffic_source
            if hasattr(lead, 'traffic_source') else '',
            converted_by=request.user,
            converted_at=timezone.now(),
            email=lead.email,
            created_by=request.user,
            team=team
        )

        lead.convert_to_client = True
        lead.save()

        messages.success(request,
                         f"{client.first_name} has been converted to a Client! Update their details.")
        return redirect('clients:edit', pk=client.pk)