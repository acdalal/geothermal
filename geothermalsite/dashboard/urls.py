from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tempvstime/", views.tempVsTime, name="tempvstime"),
    path("tempvsdepth/", views.tempVsDepth, name="tempvsdepth"),
    path("about/", views.about, name="about"),
    path("documentation/", views.documentation, name="documentation"),
]
