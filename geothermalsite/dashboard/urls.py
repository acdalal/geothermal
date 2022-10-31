from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tempvsdepth/", views.getTempVsDepthResults, name="tempvsdepth"),
    path("count/", views.countMeasurement, name="count"),
]
