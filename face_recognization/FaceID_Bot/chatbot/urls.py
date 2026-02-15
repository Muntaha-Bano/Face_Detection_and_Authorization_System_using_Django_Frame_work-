from django.urls import path
from .views import chatbot_view, logout_view, clear_chat_view

app_name = 'chatbot'

urlpatterns = [
    path('', chatbot_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('clear-chat/', clear_chat_view, name='clear_chat'),
]

