from django.contrib import admin
from .models import Assignment, Submission, Quiz, QuizQuestion, QuizAnswer

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)
