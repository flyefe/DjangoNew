from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.urls import reverse_lazy, reverse

from .models import Lead, LeadComment
from .forms import AddLeadForm, AddCommentForm

from django.contrib import messages
from django.utils import timezone
from client.models import Client
from team.models import Team





class CommentEditView(UpdateView):
    model = LeadComment
    form_class = AddCommentForm
    template_name = 'lead/edit_comment.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the comment. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('leads:detail', kwargs={'pk': self.object.lead.pk})
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = LeadComment
    template_name = 'lead/comment_confirm_delete.html'
    
    def get_success_url(self):
            return reverse_lazy('leads:detail', kwargs={'pk': self.object.lead.pk})

    def get_object(self, queryset=None):
        # Retrieve the comment object using the primary key from the URL
        pk = self.kwargs.get('pk')
        return get_object_or_404(LeadComment, pk=pk)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.created_by != request.user:
            return self.handle_no_permission()
        return super().delete(request, *args, **kwargs)
    

class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        # Initialize the form with POST data
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            # Retrieve the team and create a new comment
            team = Team.objects.filter(created_by=request.user).first()
            if not team:
                messages.error(request, "You don't have a team assigned.")
                return redirect('leads:detail', pk=pk)
            
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
            
            messages.success(request, "Comment added successfully.")
        else:
            # If form is not valid, send error messages
            messages.error(request, "There was an error with your comment submission. Please try again.")

        return redirect('leads:detail', pk=pk)

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team'] = Team.objects.filter(created_by=self.request.user).first()
        return context
    

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
    success_url = reverse_lazy('leads:detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm
        return context


    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Lead, created_by=self.request.user, pk=pk)
    


    




class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

    def get_queryset(self):      
        return  Lead.objects.filter(created_by=self.request.user, convert_to_client=False)



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