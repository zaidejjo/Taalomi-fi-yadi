from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Student, Teacher, GradeLevel

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'national_id', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'national_id', 'first_name', 'last_name')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'national_id', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    search_fields = ('name',)
    list_filter = ('year',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'national_id', 'grade', 'section', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email', 'user__national_id')
    list_filter = ('grade', 'section')

    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def national_id(self, obj):
        return obj.user.national_id

    def phone(self, obj):
        return obj.user.phone


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'national_id', 'specialty', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email', 'user__national_id', 'specialty')

    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email

    def national_id(self, obj):
        return obj.user.national_id

    def phone(self, obj):
        return obj.user.phone
