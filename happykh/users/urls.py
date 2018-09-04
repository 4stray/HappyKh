"""Urls to views for app users"""
from django.urls import path
from users import views

urlpatterns = [
    path('api/users/login/', views.UserLogin.as_view()),
]
