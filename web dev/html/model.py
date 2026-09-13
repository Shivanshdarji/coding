from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Progress from 0 to 100

    def __str__(self):
        return f"{self.user.username} - {self.activity.name} - {self.progress}%"
