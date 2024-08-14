from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.views import View


from django.contrib import messages
from django.urls import reverse_lazy, reverse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Client, ClientComment
from .forms import AddClientForm, AddCommentForm
from team.models import Team
# from lead.models import Lead



class CommentEditView(UpdateView):
    model = ClientComment
    form_class = AddCommentForm
    template_name = 'client/edit_comment.html'

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating the comment. Please try again.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('clients:detail', kwargs={'pk': self.object.client.pk})
    


class CommentDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClientComment
    # success_url = reverse_lazy('clients:detail')
    success_message = "%(content)s has been deleted."

    def get_queryset(self):
        return ClientComment.objects.filter(created_by=self.request.user)
    
    def get_success_url(self):
        # Assuming `lead` is a ForeignKey on the `ClientComment` model
        client_pk = self.object.client.pk
        return reverse_lazy('clients:detail', kwargs={'pk': client_pk})
    
    def get_success_message(self, cleaned_data):
        return f"Comment by {self.object.created_by} has been deleted."
    

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.get_success_message(None))
        return super().delete(request, *args, **kwargs)

class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    success_message = "%(first_name)s has been deleted."

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)
    
    def get_success_message(self, cleaned_data):
        return f"{self.object.first_name} has been deleted."

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, self.get_success_message(None))
        return super().delete(request, *args, **kwargs)


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
    # Get the client object for the current user
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user).first()

    # Handle form submission
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client  # Assign the comment to the client
            comment.save()
            return redirect('clients:detail', pk=pk)  # Redirect to the client detail page
    else:
        form = AddCommentForm()

    return render(request, 'client/client_detail.html', {
        'client': client,
        'form': form,
    })


# @login_required
# def client_list(request):
#     # if team_id is None:
#     #     messages.success(
#     #         request, f"there is no team associated to this request"
#     #     )

#     #     return redirect('userprofiles:error')
    
#     team = get_object_or_404(Team, id=team_id, members=request.user)
#     clients = Client.objects.filter(team=team)

#     return render(request, 'client/client_list.html', {
#             'clients': clients,
#             'team' : team,
#         }
#         )

@login_required
def client_list(request):
    clients = Client.objects.all()  # Fetch all clients without filtering by team

    return render(request, 'client/client_list.html', {
        'clients': clients,
    })


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
