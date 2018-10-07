"""Creation model for place"""

from django.db import models
from users.models import User
from utils import make_upload_image


def make_upload_logo(instance, filename):
    """
    Function which creates path for place's logo.
    Should be used as base-function for function in parameter upload_to of
    ImageField.

    :param instance: instance of Place
    :param filename: name of the user's file, ex. 'image.png'
    :return: path to image or None if filename is empty
    """

    return make_upload_image(filename, 'place/logo')


class Place(models.Model):
    """
    Place model for creation new places
    """

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
