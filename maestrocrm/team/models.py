from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, related_name='created_teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='teams')

  

    def __str__(self):
        return self.name