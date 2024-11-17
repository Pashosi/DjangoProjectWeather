from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [
    path('', views.WeatherHome.as_view(), name='index'),
    path('search/', views.WeatherResultsView.as_view(), name='search'),
    path('add_location/', views.AddLocationView.as_view(), name='add_location'),
]