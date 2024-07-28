from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    #Current Services
    GENERAL = 'general'
    UK_VISA = 'uk visa'
    CANADA_VISA =  'canada visa'
    STUDY = 'study'

    #list to choose from for priority of customers
    CHOICES_SERVICE = (
        (GENERAL, 'General'),
        (UK_VISA, 'Uk Visa'),
        (CANADA_VISA, 'Canada Visa'),
        (STUDY, 'Study' ),
    )

    name = models.CharField(max_length=225)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    service = models.CharField(max_length=20, choices=CHOICES_SERVICE, default=GENERAL)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClientNote(models.Model):
    clieint = models.ForeignKey(Client, related_name='notes', on_delete=models.CASCADE)
    note = models.TextField()
    created_by = models.ForeignKey(User, related_name='client_notes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Note by {self.created_by.username} on {self.created_at}'