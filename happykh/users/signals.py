import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import User
from utils import delete_std_images_from_media

LOGGER = logging.getLogger('happy_logger')


@receiver(pre_delete, sender=User)
def delete_media_files(sender, instance, using, **kwargs):
    LOGGER.info('Deleted files of user in signal.')
    delete_std_images_from_media(instance.profile_image,
                                 sender.VARIATIONS_PROFILE_IMAGE)
