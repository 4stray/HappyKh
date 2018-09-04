from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^api/users/login$', views.UserLogin.as_view()),
]