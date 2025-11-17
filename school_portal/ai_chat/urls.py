from django.urls import path
from . import views

app_name = 'ai_chat'
urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('chat_ai/', views.chat_ai, name='chat_ai'),
]
