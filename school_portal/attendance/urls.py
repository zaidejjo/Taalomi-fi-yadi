from django.urls import path
from . import views

app_name = 'attendance'  # ← مهم جداً

urlpatterns = [
    path('', views.absence_list, name='absence_list'),
    path('add/', views.add_absence, name='add_absence'),
]
