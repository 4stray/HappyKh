"""Urls to api's views for app places"""
from django.urls import path, include

from . import views

urlpatterns = [ #pylint: disable = invalid-name
    path('places/', include([
         path('', views.PlacePage.as_view()),
         path('<int:place_id>', views.PlaceSinglePage.as_view()),
         ])),
    ]
