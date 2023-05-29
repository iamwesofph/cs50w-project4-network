
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("tweet", views.tweet, name="tweet"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<int:id>", views.follow, name="follow"), # Id of user to follow
    path("update/<int:id>", views.update, name="update"), # Id of post to update
    path("like/<int:post_id>", views.like, name="like"), # Id of post to like  # API endpoint
]
