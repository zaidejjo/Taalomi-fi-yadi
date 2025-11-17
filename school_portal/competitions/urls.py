from django.urls import path
from . import views

app_name = 'competitions'
urlpatterns = [
    path('', views.competition_list, name='competition_list'),
    path('<int:competition_id>/', views.competition_detail, name='competition_detail'),
]
