from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # المواد
    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/<int:grade_number>/<str:subject_name>/', views.subject_detail_view, name='subject_detail'),

    # عرض تفاصيل الدرس
    path(
        'lesson/<int:pk>/',
        views.LessonDetailView.as_view(),
        name='lesson_detail'
    ),

    # الجدول
    path('timetable/', views.timetable_view, name='timetable'),

    # الامتحانات
    path('exams/', views.ExamListView.as_view(), name='exams'),

    # الدرجات
    path('grades/', views.GradeListView.as_view(), name='grades'),
    path(
        'subjects/<int:grade_number>/<str:subject_name>/lesson/<int:lesson_number>/',
        views.lesson_video_view,
        name='lesson_video'
    ),
]


"""
from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # الصفحة الرئيسية للأكاديمية
    path('', views.IndexView.as_view(), name='index'),

    # -------------------- المواد --------------------
    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/<int:grade_number>/<str:subject_name>/', views.subject_detail_view, name='subject_detail'),
    path('subjects/add/', views.SubjectCreateView.as_view(), name='add_subject'),
    path('subjects/edit/<int:pk>/', views.SubjectUpdateView.as_view(), name='edit_subject'),
    path('subjects/delete/<int:pk>/', views.SubjectDeleteView.as_view(), name='delete_subject'),

    # -------------------- الدروس --------------------
    path('lesson/<int:lesson_id>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/add/', views.LessonCreateView.as_view(), name='add_lesson'),
    path('lesson/edit/<int:pk>/', views.LessonUpdateView.as_view(), name='edit_lesson'),
    path('lesson/delete/<int:pk>/', views.LessonDeleteView.as_view(), name='delete_lesson'),

    # -------------------- الجدول الدراسي --------------------
    path('timetable/', views.timetable_view, name='timetable'),
    path('timetable/add/', views.TimetableSlotCreateView.as_view(), name='add_timetable_slot'),
    path('timetable/edit/<int:pk>/', views.TimetableSlotUpdateView.as_view(), name='edit_timetable_slot'),
    path('timetable/delete/<int:pk>/', views.TimetableSlotDeleteView.as_view(), name='delete_timetable_slot'),

    # -------------------- الامتحانات --------------------
    path('exams/', views.ExamListView.as_view(), name='exams'),
    path('exams/add/', views.ExamCreateView.as_view(), name='add_exam'),
    path('exams/edit/<int:pk>/', views.ExamUpdateView.as_view(), name='edit_exam'),
    path('exams/delete/<int:pk>/', views.ExamDeleteView.as_view(), name='delete_exam'),

    # -------------------- الدرجات --------------------
    path('grades/', views.GradeListView.as_view(), name='grades'),
    path('grades/add/', views.GradeCreateView.as_view(), name='add_grade'),
    path('grades/edit/<int:pk>/', views.GradeUpdateView.as_view(), name='edit_grade'),
    path('grades/delete/<int:pk>/', views.GradeDeleteView.as_view(), name='delete_grade'),
]

"""