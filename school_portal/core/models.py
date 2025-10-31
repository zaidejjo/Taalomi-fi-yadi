from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# ===========================
# نموذج المستخدم الأساسي
# ===========================
class User(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, verbose_name=_('الاسم الثاني'))
    third_name = models.CharField(max_length=30, blank=True, verbose_name=_('الاسم الثالث'))

    class Role(models.TextChoices):
        STUDENT = 'student', _('طالب')
        TEACHER = 'teacher', _('معلم')
        MANAGER = 'manager', _('مدير المدرسة')

    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name=_('الدور')
    )
    national_id = models.CharField(max_length=20, unique=True, verbose_name=_('الرقم الوطني'))
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name=_("صورة الملف الشخصي"))

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        indexes = [models.Index(fields=['national_id']), models.Index(fields=['username'])]

    def __str__(self):
        full_name = f"{self.first_name} {self.middle_name} {self.third_name}".strip()
        return f"{full_name or self.username} ({self.get_role_display()})"


# ===========================
# الصفوف الدراسية
# ===========================
class GradeLevel(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('الصف'))
    year = models.IntegerField(verbose_name=_('السنة الدراسية'))

    class Meta:
        verbose_name = _('مرحلة/صف')
        verbose_name_plural = _('المراحل/الصفوف')
        ordering = ['year', 'name']

    def __str__(self):
        return f"{self.name} ({self.year})"


# ===========================
# نموذج الطالب
# ===========================
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', verbose_name=_('مستخدم'))
    grade = models.ForeignKey(GradeLevel, on_delete=models.PROTECT, verbose_name=_('الصف'))
    section = models.CharField(max_length=10, default='A', verbose_name=_('الشعبة/الفصل'))

    class Meta:
        verbose_name = _('طالب')
        verbose_name_plural = _('الطلاب')
        unique_together = (('user',),)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.grade} {self.section}"


# ===========================
# نموذج المعلم
# ===========================
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', verbose_name=_('مستخدم'))
    specialty = models.CharField(max_length=100, blank=True, verbose_name=_('تخصص'))

    class Meta:
        verbose_name = _('معلم')
        verbose_name_plural = _('المعلمون')

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# ===========================
# نموذج مدير المدرسة
# ===========================
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager', verbose_name=_('مستخدم'))
    office = models.CharField(max_length=100, blank=True, verbose_name=_('المكتب/المسمى الوظيفي'))

    class Meta:
        verbose_name = _('مدير المدرسة')
        verbose_name_plural = _('مدراء المدارس')

    def __str__(self):
        return self.user.get_full_name() or self.user.username
