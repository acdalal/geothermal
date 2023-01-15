from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("tempvsdepth/", views.getTempVsDepthResults, name="tempvsdepth"),
    # path("count/", views.countMeasurement, name="count"),
    path("tempvstime/", views.tempVsTime, name="tempvstime"),
    path("tempvsdepth/", views.tempVsDepth, name="tempvsdepth"),
    path("tempvstime/download", views.tempVsTimeDownload, name="tempvstimedownload"),
    path("tempvsdepth/download", views.tempVsDepthDownload, name="tempvsdepthdownload"),
    path("about/", views.about, name="about"),
]
