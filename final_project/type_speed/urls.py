
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("results/", views.process_results, name="process_results")
    
]