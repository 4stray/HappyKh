"""Module for registration app"""
from django.apps import AppConfig


class PlacesConfig(AppConfig):
    """Class for places app registration"""
    name = 'places'

    def ready(self):
    # pylint: disable = unused-variable
        import places.signals
