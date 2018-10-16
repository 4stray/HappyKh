"""Functions and classes which are used in different apps"""

import os
import uuid

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from rest_framework import serializers


def make_upload_image(filename, path):
    """
    Function which creates path for user's file in media folder using uuid.

    :param filename: name of the user's file, ex. 'image.png'
    :param path: where to save file in media folder, ex. 'model/attr'
    :return: path to file or None if filename is empty
    """
    if filename:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return f'{path}/{filename[0]}/{filename[2]}/{filename}'
    return None


def delete_std_images_from_media(std_image_file, variations):
    """
    Delete images which were created by StdImageField.

    :param std_image_file: instance of StdImageFile from
    django-stdimage library
    :param variations: iterable obj with names of declared variations for
                        std_image_file
    :return: None
    """
    path = std_image_file.path.split('media/')[-1]
    os.remove(
        os.path.join(settings.MEDIA_ROOT, path))
    for variant in variations:
        extension = path.split('.')[-1]
        filename = path.split('.')[0]
        path_to_variant_file = f'{filename}.{variant}.{extension}'
        os.remove(
            os.path.join(settings.MEDIA_ROOT, path_to_variant_file))


class UploadedImageField(serializers.ImageField):
    """
    Class which converts a base64 string to a file when input and converts
    image
    by path to it into base64 string
    """

    def to_internal_value(self, data):
        if isinstance(data, UploadedFile):
            data = ContentFile(data.read(), name=data.name)
        if data == 'undefined':
            return None
        return super(UploadedImageField, self).to_internal_value(data)

    def to_representation(self, image_field):
        domain_site = self.context.get('domain')
        if image_field and domain_site:
            domain = 'http://' + str(domain_site)
            original_url = image_field.url
            variation = self.context['variation']
            if variation:
                extension = original_url.split('.')[-1]
                original_url = original_url.split('.')[0]
                image_url = f"{domain}{original_url}.{variation}.{extension}"
            else:
                image_url = f"{domain}{original_url}"
            return image_url
        return ''
