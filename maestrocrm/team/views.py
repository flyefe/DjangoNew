from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages

from .models import Team
from .forms import AddTeamForm




@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = AddTeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()
            
            messages.success(request, f"{team.name} has been edited successfully.")
            return redirect('myaccount')
        else:
            messages.success(request, f" form is not valid")
            return render(request, 'team/edit_team.html', {
                'team': team,
                'form': form,})
    
    else:
         form = AddTeamForm(instance=team)
         return render(request, 'team/edit_team.html', {
            'team':team,
            'form' : form
            })

