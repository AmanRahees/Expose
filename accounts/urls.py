from django.urls import path
from . import views

urlpatterns = [
    path('', views.Userlogin, name='login'),
    path('otplogin/', views.otplogin, name='otplogin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.User_logout, name='logout'),
    path('verification/', views.otpVerification, name='verification'),
    path('change_password/', views.ChangePassword, name='change_password'),
    path('forgot_password/', views.ForgotPassword, name='forgot_password'),
    path('resetPassword/', views.reset_password, name='resetPassword'),
    path('resend_otp/', views.resendotp, name='resend'),


    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
]