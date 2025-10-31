from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('grade-levels/', views.GradeLevelListView.as_view(), name='gradelevel_list'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]
