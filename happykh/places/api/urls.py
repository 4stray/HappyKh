"""Urls to api's views for app places"""
from django.urls import path, include

from . import views

urlpatterns = [
    path('places/', include([
        path('', views.PlacePage.as_view()),
        path('<int:place_id>', views.PlaceSinglePage.as_view()),
        path('<int:place_id>/comments', views.CommentsAPI.as_view()),
        path(
            '<int:place_id>/editing_permission',
            views.PlacesEditingPermissions.as_view()
        ),
        path('rating/<int:place_id>', views.PlaceRatingView.as_view()),
    ])),
]
