from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('adoption/', views.adoption_feed, name='adoption_feed'),
    path('adoption/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pet_id>/apply/', views.application_form, name='application_form'),
    path('messages/', views.chat_list, name='chat_list'),
    path('messages/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/settings/', views.account_settings, name='account_settings'),
    path('my-pets/<int:pet_id>/', views.pet_profile, name='pet_profile'),
    path('my-pets/<int:pet_id>/edit/', views.pet_edit, name='pet_edit'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/report/', views.report, name='report'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
