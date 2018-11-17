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
            views.PlacesEditingPermission.as_view()
        ),
        path(
            '<int:place_id>/editing_permission_request',
            views.PlacesEditingPermissionRequest.as_view()
        ),
        path('<int:place_id>/comments/<int:comment_id>',
             views.SingleCommentAPI.as_view()),
        path('rating/<int:place_id>', views.PlaceRatingView.as_view()),
    ])),
]
