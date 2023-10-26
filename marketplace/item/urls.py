from django.urls import path
from . import views


app_name = "item"

urlpatterns = [
    path("", views.items, name="items"),
    path("new/", views.newItem, name="new_item"),
    path("<int:pk>", views.details, name="details"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/edit/", views.editItem, name="edit"),
]
