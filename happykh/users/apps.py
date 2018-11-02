""" Module for registration app """
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Class for users app registration"""
    name = 'users'

    def ready(self):
        import users.signals
