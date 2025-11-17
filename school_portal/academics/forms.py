# academies/forms.py
from django import forms
from .models import Subject, Lesson, TimetableSlot, Exam, Grade

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

class TimetableSlotForm(forms.ModelForm):
    class Meta:
        model = TimetableSlot
        fields = '__all__'

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
