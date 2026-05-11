from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index2/<int:val1>/", views.index2, name="index2"),
    path("search", views.searchBooks, name="searchBooks"),
    path("simple/query", views.simple_query, name="simple_query"),
    path("complex/query", views.complex_query, name="complex_query"),
]
