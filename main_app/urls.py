from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login_register", views.login_register),
    path("register", views.register),
    path("login", views.login),
    path("logout", views.logout),
    path("dashboard", views.dashboard),
    path("recipes", views.recipes),
    path("recipes/create", views.create),
    path("recipes/process_create", views.process_create),
    path("recipes/<int:recipe_id>", views.view_recipe),
    path("recipes/<int:recipe_id>/edit", views.edit),
    path("recipes/<int:recipe_id>/process_edit", views.process_edit),
    path("recipes/<int:recipe_id>/destroy", views.delete),
    path("recipes/<int:recipe_id>/favorite", views.favorite),
    path("recipes/<int:recipe_id>/remove_favorite", views.remove_favorite),
    path("recipes/<int:recipe_id>/comment", views.comment),
    path("recipes/<int:recipe_id>/<int:comment_id>/destroy_comment", views.delete_comment),
]