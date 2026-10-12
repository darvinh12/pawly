from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/profile/', views.profile_form, name='profile_form'),
    path('password-reset/', views.password_reset, name='password_reset'),
]
