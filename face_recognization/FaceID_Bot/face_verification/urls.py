from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.face_login, name='login'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('capture_face/', views.capture_face, name='capture_face'),
    path('capture_face_from_camera/', views.capture_face_from_camera, name='capture_face_from_camera'),
    path('check_user/', views.check_existing_user, name='check_user'),
    path('login-user/', views.login_user, name='login_user'),
    path('register_user/', views.register_user, name='register_user'),
    path('get_captured_image/', views.get_captured_image, name='get_captured_image'),
]
