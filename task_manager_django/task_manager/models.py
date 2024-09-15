from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

class Task(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)  # False for pending, True for completed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    class Meta:
        db_table = "Task"




