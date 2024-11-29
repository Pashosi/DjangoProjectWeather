from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [
    path('', views.WeatherHome.as_view(), name='index'),
    path('search/', views.WeatherSearchView.as_view(), name='search'),
]