from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("documentation/", views.documentation, name="documentation"),
    path("customquery/", views.customQuery, name="customquery"),
]
