import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from places.models import Place
from utils import delete_std_images_from_media

LOGGER = logging.getLogger('happy_logger')


@receiver(pre_delete, sender=Place)
def delete_media_files(sender, instance, using, **kwargs):
    LOGGER.info('Deleted files of place in signal.')
    delete_std_images_from_media(instance.logo,
                                 sender.VARIATIONS_LOGO)
