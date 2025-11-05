from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import GradeLevel, Teacher, Student


class Weekday(models.IntegerChoices):
    SUNDAY = 0, _('الأحد')
    MONDAY = 1, _('الاثنين')
    TUESDAY = 2, _('الثلاثاء')
    WEDNESDAY = 3, _('الأربعاء')
    THURSDAY = 4, _('الخميس')
    FRIDAY = 5, _('الجمعة')
    SATURDAY = 6, _('السبت')


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('اسم المادة'))
    grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, verbose_name=_('الصف'))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_('المعلم'), null=True, blank=True)

    class Meta:
        verbose_name = _('مادة')
        verbose_name_plural = _('المواد')

    def __str__(self):
        return f"{self.name} - {self.grade}"


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('المادة'))
    date = models.DateField(verbose_name=_('التاريخ'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان الدرس'))
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name=_('فيديو'))
    materials = models.FileField(upload_to='materials/', blank=True, null=True, verbose_name=_('مرفقات'))

    class Meta:
        verbose_name = _('درس')
        verbose_name_plural = _('دروس')
        ordering = ['-date', 'title']

    def __str__(self):
        return f"{self.title} - {self.subject}"


class TimetableSlot(models.Model):
    grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, verbose_name=_('الصف'))
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name=_('المادة'))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_('المعلم'))
    weekday = models.IntegerField(choices=Weekday.choices, verbose_name=_('اليوم'))
    start_time = models.TimeField(verbose_name=_('وقت البدء'))
    end_time = models.TimeField(verbose_name=_('وقت الانتهاء'))

    class Meta:
        verbose_name = _('حصة')
        verbose_name_plural = _('الجدول الدراسي')
        ordering = ['weekday', 'start_time']

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.subject} ({self.start_time}-{self.end_time})"


class Exam(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('المادة'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان الامتحان'))
    date = models.DateField(verbose_name=_('تاريخ الامتحان'))

    class Meta:
        verbose_name = _('امتحان')
        verbose_name_plural = _('الامتحانات')
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.subject} ({self.date})"


class Grade(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_('الامتحان'))
    student = models.ForeignKey('core.Student', on_delete=models.CASCADE, related_name='exam_grades', verbose_name=_('الطالب'))
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('الدرجة'))
    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))

    class Meta:
        verbose_name = _('درجة')
        verbose_name_plural = _('الدرجات')
        unique_together = (('exam', 'student'),)

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.score}"
