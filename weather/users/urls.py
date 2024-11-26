from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
]