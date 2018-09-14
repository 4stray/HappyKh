"""Urls to api's views for app users"""
from django.urls import path, include
from users.api import views


urlpatterns = [
    path('users/', include([
        path('login/', views.LoginView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('registration/', views.UserRegistration.as_view()),
        path('activate/<int:user_id>/<slug:token>/',
             views.UserActivation.as_view()),
    ])),
]
