"""Creation model for place"""
from django.db import models
from users.models import User

class Place(models.Model):
    """
    Place model for creation new places
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.TextField(blank=True)

    def __str__(self):
        return self.name
