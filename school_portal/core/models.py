# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# ===========================
# نموذج الصفوف (Grade Level)
# ===========================
class GradeLevel(models.Model):
    name = models.CharField(max_length=50, verbose_name="اسم الصف", unique=True)

    class Meta:
        verbose_name = "صف"
        verbose_name_plural = "الصفوف"

    def __str__(self):
        return self.name


# ===========================
# نموذج المستخدم الأساسي
# ===========================
class User(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name=_('الاسم الأول'))
    second_name = models.CharField(max_length=30, blank=True, verbose_name=_('الاسم الثاني'))
    third_name = models.CharField(max_length=30, blank=True, verbose_name=_('الاسم الثالث'))
    fourth_name = models.CharField(max_length=30, blank=True, verbose_name=_('الاسم الرابع'))
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name=_('الرقم الوطني'))

    class Role(models.TextChoices):
        STUDENT = 'student', _('طالب')
        TEACHER = 'teacher', _('معلم')
        MANAGER = 'manager', _('مدير المدرسة')

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name=_('الدور'))
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name=_("صورة الملف الشخصي"))

    # USERNAME_FIELD الافتراضي يظل 'username' → للسوبر يوزر التقليدي
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        indexes = [models.Index(fields=['national_id'])]

    def __str__(self):
        full_name = f"{self.first_name} {self.second_name} {self.third_name} {self.fourth_name}".strip()
        return f"{full_name} ({self.get_role_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.second_name} {self.third_name} {self.fourth_name}".strip()


# ===========================
# نموذج الطالب
# ===========================
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    grade = models.ForeignKey(GradeLevel, on_delete=models.SET_NULL, null=True, verbose_name='الصف')
    section = models.CharField(max_length=10, default='A', verbose_name='الشعبة')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.grade} ({self.section})"


# ===========================
# نموذج المعلم
# ===========================
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    specialty = models.CharField(max_length=100, blank=True, verbose_name='تخصص')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialty}"


# ===========================
# نموذج المدير
# ===========================
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')
    office = models.CharField(max_length=100, blank=True, verbose_name='المكتب')

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.office}"
