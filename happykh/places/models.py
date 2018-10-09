"""Creation model for place"""

from django.db import models
from users.models import User
from stdimage import models as std_models
from utils import make_upload_image


class Place(models.Model):
    """
    Place model for creation new places
    """

    VARIATIONS_LOGO = {
        'large': (600, 400),
        'thumbnail': (100, 100, True),
        'medium': (300, 200),
    }

    def _make_upload_logo(self, filename):
        """
        Function which creates path for place's logo.
        Should be used as base-function for function in parameter upload_to of
        ImageField.

        :param self: instance of Place
        :param filename: name of the user's file, ex. 'image.png'
        :return: path to image or None if filename is empty
        """

        return make_upload_image(filename, 'place/logo')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = std_models.StdImageField(
        upload_to=_make_upload_logo,
        blank=True,
        null=True,
        default='',
        variations=VARIATIONS_LOGO,
    )

    def __str__(self):
        return self.name
