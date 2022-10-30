from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.getTempVsDepthResults, name='test'),
    path('count/', views.countMeasurement, name='count')
]