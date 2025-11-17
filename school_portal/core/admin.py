from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Student, Teacher, Manager, GradeLevel

# ===========================
# إدارة المستخدم
# ===========================
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'national_id', 'is_active')
    list_editable = ('role',)  # <-- هذا يسمح بتغيير الدور مباشرة من القائمة
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'national_id', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'second_name', 'third_name', 'fourth_name', 'email', 'national_id', 'profile_image')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# ===========================
# إدارة الصفوف الدراسية
# ===========================
@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

# ===========================
# إدارة الطلاب
# ===========================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'national_id', 'grade', 'section')
    search_fields = ('user__first_name', 'user__second_name', 'user__third_name', 'user__fourth_name',
                     'user__username', 'user__email', 'user__national_id')
    list_filter = ('grade', 'section')

    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def national_id(self, obj):
        return obj.user.national_id

# ===========================
# إدارة المعلمين
# ===========================
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'national_id', 'specialty')
    search_fields = ('user__first_name', 'user__second_name', 'user__third_name', 'user__fourth_name',
                     'user__username', 'user__email', 'user__national_id', 'specialty')

    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def national_id(self, obj):
        return obj.user.national_id

# ===========================
# إدارة المديرين
# ===========================
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'national_id', 'office')
    search_fields = ('user__first_name', 'user__second_name', 'user__third_name', 'user__fourth_name',
                    'user__username', 'user__email', 'user__national_id', 'office')

    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def national_id(self, obj):
        return obj.user.national_id
