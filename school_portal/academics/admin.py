from django.contrib import admin
from .models import Subject, Lesson, TimetableSlot, Exam, Grade

admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(TimetableSlot)
admin.site.register(Exam)
admin.site.register(Grade)
