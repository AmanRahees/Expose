from django.urls import path
from . import views

urlpatterns = [
    path('', views.Userlogin, name='login'),
    path('otplogin/', views.otplogin, name='otplogin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.User_logout, name='logout'),
    path('verification/', views.otpVerification, name='verification'),
    path('change_password/', views.ChangePassword, name='change_password'),
]