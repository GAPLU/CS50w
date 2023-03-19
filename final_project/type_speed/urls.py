
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("results/", views.process_results, name="process_results"),
    path("new_text", views.create_text, name="create_text"),
    path("custom", views.custom, name="custom"),

    #APIs
    path("text/<str:id>", views.send_text, name="send_text"),
    path("ranking/<str:mode>", views.filtered, name="filtered"),
    path('get_rank/<str:chars>/<str:mode>', views.get_rank, name='get_rank'),

]