from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('signup/', views.custom_signup, name='custom_signup'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('edit-profile-extended/', views.edit_profile_extended, name='edit_profile_extended'),
]

