from django.contrib.auth.models import User
from django.db import models
from core.models import BaseModel

class Lead(BaseModel):
    # Lead priority for priority of customers
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    # List to choose from for priority of customers
    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    # Lead property for customer status
    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'
    # List to choose from for customer status
    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=MEDIUM)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
    

    def convert_to_client(self, user):
        client = Client.objects.create(
            first_name=self.first_name,
            email=self.email,
            description=self.description,
            created_by=user,
            assigned_to=user,
            traffic_source='',  # Assuming you want to set a default value or copy from Lead if available
            converted_by=user,
            converted_at=timezone.now(),
        )
        return client

class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, related_name='notes', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=225)  # New field for first name
    note = models.TextField()
    created_by = models.ForeignKey(User, related_name='lead_notes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Note by {self.created_by.username} on {self.created_at}'
