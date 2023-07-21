from django.db import models
import uuid

# Create your models here.

class Request(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    emp_id = models.IntegerField()
    author = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    resolved_by = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    vacation_start_date = models.DateField()
    vacation_end_date = models.DateField()

    def __str__(self):
        return self.author