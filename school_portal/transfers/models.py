from django.db import models
from core.models import Student, GradeLevel

class Transfer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, related_name='from_transfers')
    to_grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, related_name='to_transfers')
    reason = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending','قيد المعالجة'),('approved','موافق'),('rejected','مرفوض')], default='pending')
