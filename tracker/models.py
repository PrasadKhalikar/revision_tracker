# tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_added = models.DateField(default=date.today)  # Automatically set to today
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        # Set completed_date when topic is marked as completed
        if self.completed and not self.completed_date:
            self.completed_date = date.today()
        elif not self.completed:
            self.completed_date = None  # Reset if unmarked
        super().save(*args, **kwargs)
