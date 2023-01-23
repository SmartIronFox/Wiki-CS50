from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("New/", views.NewPage, name="new"), 
    path("edit/<str:title>", views.EditPage, name="edit"),
    path("random/", views.RandomEntry, name="random")
]
