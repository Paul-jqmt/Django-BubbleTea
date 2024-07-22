from django.urls import path
# from django.shortcuts import render
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# configuration des routes
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('cookie/', views.cookie, name="index"),
    path('profile/', views.profile, name="profile"),
    path('home/', views.home, name="home"),
    path('index/', views.index, name="index"),
    path('logout/', views.logout, name="logout")
]