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

            messages.success(request,
                             f"{team.name} has been edited successfully.")
            return redirect('userprofile:myaccount')
        else:
            messages.success(request, f" form is not valid")
            return render(request, 'team/edit_team.html', {
                'team': team,
                'form': form,
            })

    else:
        form = AddTeamForm(instance=team)
        return render(request, 'team/edit_team.html', {
            'team': team,
            'form': form
        })
@login_required
def manage_team_membership(request):
    user = request.user
    available_teams = Team.objects.all()  # or filter as needed
    user_teams = user.teams.all()
    
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        action = request.POST.get('action')
        team = get_object_or_404(Team, id=team_id)

        if action == 'join':
            team.members.add(user)
            messages.success(request, f'You have joined the team: {team.name}')
        elif action == 'leave':
            team.members.remove(user)
            messages.success(request, f'You have left the team: {team.name}')
        else:
            messages.error(request, 'Invalid action.')
        
        return redirect('manage_team_membership')

    return render(request, 'team/manage_membership.html', {
        'available_teams': available_teams,
        'user_teams': user_teams,
    })