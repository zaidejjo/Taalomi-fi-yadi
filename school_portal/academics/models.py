# academies/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import GradeLevel, Teacher, Student

# ================== أيام الأسبوع ==================
class Weekday(models.IntegerChoices):
    SUNDAY = 0, _('الأحد')
    MONDAY = 1, _('الاثنين')
    TUESDAY = 2, _('الثلاثاء')
    WEDNESDAY = 3, _('الأربعاء')
    THURSDAY = 4, _('الخميس')
    FRIDAY = 5, _('الجمعة')
    SATURDAY = 6, _('السبت')


# ================== المواد ==================
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('اسم المادة'))
    grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, verbose_name=_('الصف'))
    section = models.CharField(max_length=5, blank=True, verbose_name=_('الشعبة'))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_('المعلم'), null=True, blank=True)
    description = models.TextField(blank=True, verbose_name=_('الوصف'))

    class Meta:
        verbose_name = _('مادة')
        verbose_name_plural = _('المواد')
        unique_together = ('name', 'grade', 'section')

    def __str__(self):
        return f"{self.name} - {self.grade} {self.section}"


# ================== الدروس ==================
class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('المادة'))
    date = models.DateField(verbose_name=_('التاريخ'), null=True, blank=True)
    unit = models.CharField(max_length=100, blank=True, verbose_name=_('الوحدة'))
    order = models.PositiveIntegerField(default=1, verbose_name=_('رقم الدرس'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان الدرس'))
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name=_('فيديو'))
    video_url = models.URLField(blank=True, null=True, verbose_name=_('رابط الفيديو'))

    class Meta:
        verbose_name = _('درس')
        verbose_name_plural = _('دروس')
        ordering = ['subject', 'unit', 'order', 'title']

    def __str__(self):
        return f"{self.title} - {self.subject}"


class LessonMaterial(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='materials', verbose_name=_('الدرس'))
    file = models.FileField(upload_to='materials/', verbose_name=_('مرفق'))

    class Meta:
        verbose_name = _('مرفق درس')
        verbose_name_plural = _('مرفقات الدرس')

    def __str__(self):
        return f"{self.lesson.title} - {self.file.name}"


# ================== الجدول الدراسي ==================
class TimetableSlot(models.Model):
    grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, verbose_name=_('الصف'))
    section = models.CharField(max_length=5, blank=True, verbose_name=_('الشعبة'))
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name=_('المادة'))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_('المعلم'))
    weekday = models.IntegerField(choices=Weekday.choices, verbose_name=_('اليوم'))
    start_time = models.TimeField(verbose_name=_('وقت البدء'))
    end_time = models.TimeField(verbose_name=_('وقت الانتهاء'))
    room = models.CharField(max_length=50, blank=True, verbose_name=_('الغرفة'))

    class Meta:
        verbose_name = _('حصة')
        verbose_name_plural = _('الجدول الدراسي')
        ordering = ['weekday', 'start_time']
        unique_together = ('grade', 'section', 'weekday', 'start_time')

    def __str__(self):
        return f"{self.get_weekday_display()} - {self.subject} ({self.start_time}-{self.end_time})"


# ================== الامتحانات ==================
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('نظري', _('نظري')),
        ('عملي', _('عملي')),
        ('شفوي', _('شفوي')),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_('المادة'))
    title = models.CharField(max_length=200, verbose_name=_('عنوان الامتحان'))
    date = models.DateField(verbose_name=_('تاريخ الامتحان'))
    section = models.CharField(max_length=5, blank=True, verbose_name=_('الشعبة'))
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE_CHOICES, default='نظري', verbose_name=_('نوع الامتحان'))

    class Meta:
        verbose_name = _('امتحان')
        verbose_name_plural = _('الامتحانات')
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - {self.subject} ({self.date})"


# ================== الدرجات ==================
class Grade(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, verbose_name=_('الامتحان'))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_grades', verbose_name=_('الطالب'))
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('الدرجة'))
    notes = models.TextField(blank=True, verbose_name=_('ملاحظات'))
    graded_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('قيم الدرجات'))

    class Meta:
        verbose_name = _('درجة')
        verbose_name_plural = _('الدرجات')
        unique_together = (('exam', 'student'),)

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.score}"

