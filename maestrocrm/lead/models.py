from django.contrib.auth.models import User
from django.db import models

class Lead(models.Model):
    #Lead priority for priority of customers
    LOW = 'low'
    MEDIUM =  'medium'
    HIGH = 'high'

    #list to choose from for priority of customers
    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High' ),
    )

    #lead property for customer status
    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'
    #list to choose from for customers status
    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )


    name = models.CharField(max_length=225)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=MEDIUM)
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    convert_to_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, related_name='notes', on_delete=models.CASCADE)
    note = models.TextField()
    created_by = models.ForeignKey(User, related_name='lead_notes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Note by {self.created_by.username} on {self.created_at}'