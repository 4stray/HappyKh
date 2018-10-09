import base64
import os
import uuid
import six

from django.conf import settings
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


def delete_std_images_from_media(std_image_file, variations={}):
    """
    Delete images which were created by StdImageField.

    :param std_image_file: instance of StdImageFile from django-stdimage library
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


class Base64ImageField(serializers.ImageField):
    """
    Class which converts a base64 string to a file when input and converts image
    by path to it into base64 string
    """

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

                # Try to decode the file. Return validation error if it fails.
                try:
                    decoded_file = base64.b64decode(data)
                except TypeError:
                    self.fail('invalid_image')

                # Get the file name extension:
                file_extension = header.split('/')[-1]

                # Generate file name:
                file_name = uuid.uuid4()

                complete_file_name = "%s.%s" % (file_name, file_extension,)

                data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def to_representation(self, value):
        if value:
            image_file = value.path
            if not os.path.isfile(image_file):
                return None

            encoded_string = ''
            with open(image_file, 'rb') as img_f:
                encoded_string = base64.b64encode(img_f.read())
                encoded_string = encoded_string.decode()
            extension = value.path.split('.')[-1]
            return f'data:image/{extension};base64,{encoded_string}'
        return ''
