from django.db import models
from core.models import Student

class Absence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.CharField(max_length=200, blank=True)
    excused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
