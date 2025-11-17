from django.contrib import admin
from .models import Subject, Lesson, TimetableSlot, Exam, Grade

# ----------------------------------------
# Subject Admin
# ----------------------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'teacher')
    list_filter = ('grade', 'teacher')
    search_fields = ('name',)
    ordering = ('grade', 'name')

# ----------------------------------------
# Lesson Admin
# ----------------------------------------
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'date')
    list_filter = ('subject', 'date')
    search_fields = ('title',)
    ordering = ('-date', 'title')

# ----------------------------------------
# TimetableSlot Admin
# ----------------------------------------
@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('grade', 'subject', 'teacher', 'weekday', 'start_time', 'end_time')
    list_filter = ('grade', 'teacher', 'weekday')
    ordering = ('weekday', 'start_time')

# ----------------------------------------
# Exam Admin
# ----------------------------------------
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'date')
    list_filter = ('subject', 'date')
    search_fields = ('title',)
    ordering = ('-date',)

# ----------------------------------------
# Grade Admin
# ----------------------------------------
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'score')
    list_filter = ('exam',)
    search_fields = ('student__user__username', 'student__user__first_name', 'student__user__last_name')
    ordering = ('exam', 'student')
