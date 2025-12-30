# api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/refresh/', views.refresh_token, name='token_refresh'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    

    # Folder endpoints
    path('create-folder/', views.create_folder, name='create_folder'),
    path('folders/', views.list_folders, name='list_folders'),
    
    
    # File endpoints
    path('upload-file/', views.upload_file, name='upload_file'),
    path('list-files/', views.list_files, name='list_files'),
    path('file/<int:pk>/download/', views.download_file, name='download_file'),
]