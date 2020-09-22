from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.topic, name="topic"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage"),
    path("editpage/<str:title>", views.editpage, name="editpage")
]
