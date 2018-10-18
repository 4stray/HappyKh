"""Urls to api's views for app users"""
from django.urls import path, include

from . import views

urlpatterns = [  # pylint: disable = invalid-name
    path('users/', include([
        path('login', views.UserLogin.as_view()),
        path('logout', views.UserLogout.as_view()),
        path('registration', views.UserRegistration.as_view()),
        path('activate/<int:user_id>/<slug:token>/',
             views.UserActivation.as_view()),
        path('activate/send-email/', views.UserActivation.as_view()),
        path('<int:id>', views.UserProfile.as_view()),
        path('<int:id>/data', views.UserProfile.as_view()),
        path('<int:id>/password', views.UserPassword.as_view()),
        path('<int:id>/email', views.UserEmail.as_view()),
    ])),
]
