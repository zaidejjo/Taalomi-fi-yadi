from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lesson/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/<int:grade_number>/<str:subject_name>/', views.subject_detail_view, name='subject_detail'),
    path("timetable/", views.timetable_view, name="timetable"),  # رابط الجدول الدراسي
    path('grades/', views.GradeListView.as_view(), name='grades'),
    path('exams/', views.ExamListView.as_view(), name='exams'),

]
