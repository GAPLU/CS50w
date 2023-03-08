
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<str:username>", views.user_profile, name="user_profile"),
    path("following", views.index, name="following"),

    # API Routes
    path("create_post", views.create_post, name="create_post")
]
