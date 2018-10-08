
"""Urls to api's views for app places"""
from django.urls import path, include

from . import views

urlpatterns = [ #pylint: disable = invalid-name
    path('places/', include([
         path('', views.PlacePage.as_view()),
         ])),
    ]
