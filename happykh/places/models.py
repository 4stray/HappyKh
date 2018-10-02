from django.db import models
from users.models import User

class Place(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	description = models.TextField()
	image = models.ImageField(upload_to='images/', blank=True)

	def __str__(self):
		return self.name

    
