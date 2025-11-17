# core/models.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('grade-levels/', views.GradeLevelListView.as_view(), name='gradelevel_list'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    # تسجيل الدخول والخروج
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
]
