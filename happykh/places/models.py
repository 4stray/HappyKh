"""Creation model for place"""
import uuid

from django.db import models
from users.models import User


class Place(models.Model):
    """
    Place model for creation new places
    """

    def make_upload_logo(self, filename):
        if filename:
            ext = filename.split('.')[-1]
            filename = "%s.%s" % (uuid.uuid4(), ext)
            return u'place/logo/%s/%s/%s' % (
                filename[:1], filename[2:3],
                filename)
        return None

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to=make_upload_logo,
        blank=True,
        null=True,
        default='',
    )

    def __str__(self):
        return self.name
