from django.db import models

from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    first_name = models.CharField(max_length=225)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='%(class)s_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
