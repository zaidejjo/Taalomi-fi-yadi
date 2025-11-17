from django.urls import path
from . import views

urlpatterns = [
    path('', views.transfer_list, name='transfer_list'),
    path('request/', views.request_transfer, name='request_transfer'),
    path('<int:transfer_id>/approve/', views.approve_transfer, name='approve_transfer'),
]
