# core/views.py
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django import forms
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import GradeLevel, Student, Teacher, Manager

User = get_user_model()

ROLE_CHOICES = [
    ('student', 'طالب'),
    ('teacher', 'معلم'),
    ('manager', 'مدير المدرسة'),
]

# ===========================
# نموذج تسجيل مستخدم جديد
# ===========================
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تأكيد كلمة المرور", widget=forms.PasswordInput)
    role = forms.ChoiceField(label="اختر الدور", choices=ROLE_CHOICES)
    grade = forms.ModelChoiceField(queryset=GradeLevel.objects.all(), required=False, label="الصف")
    section = forms.CharField(max_length=10, required=False, label="الشعبة")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "second_name", "third_name", "fourth_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
            if user.role == 'student':
                grade = self.cleaned_data.get('grade')
                section = self.cleaned_data.get('section') or 'A'
                Student.objects.create(user=user, grade=grade, section=section)
            elif user.role == 'teacher':
                Teacher.objects.create(user=user)
            elif user.role == 'manager':
                Manager.objects.create(user=user)
        return user

# ===========================
# عرض التسجيل
# ===========================
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        # إعادة التوجيه حسب الدور
        if user.role == 'student':
            return redirect('academics:index')
        elif user.role == 'teacher':
            return redirect('academics:exams')
        elif user.role == 'manager':
            return redirect('attendance:absence_list')
        return super().form_valid(form)

# ===========================
# الصفحة الرئيسية
# ===========================
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user_role = getattr(self.request.user, 'role', None) if self.request.user.is_authenticated else None

        # العد بدون superuser
        student_count = User.objects.filter(role='student').count()
        teacher_count = User.objects.filter(role='teacher').count()
        manager_count = User.objects.filter(role='manager', is_superuser=False).count()

        ctx.update({
            'page_title': 'الرئيسية - تعلمي في يدي',
            'grade_count': GradeLevel.objects.count(),
            'student_count': student_count,
            'teacher_count': teacher_count,
            'manager_count': manager_count,
            'show_academics': True,
            'show_exams_grades': user_role in ['teacher', 'manager'],
            'show_attendance': user_role == 'manager',
            'show_assignments': user_role in ['student', 'teacher'],
            'show_competitions': True,
        })
        return ctx

# ===========================
# الصفوف الدراسية
# ===========================
class GradeLevelListView(LoginRequiredMixin, ListView):
    model = GradeLevel
    template_name = 'core/gradelevel_list.html'
    context_object_name = 'gradelevels'
    paginate_by = 20

class GradeLevelDetailView(LoginRequiredMixin, DetailView):
    model = GradeLevel
    template_name = 'core/gradelevel_detail.html'
    context_object_name = 'grade'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['students'] = self.object.student_set.all()
        return ctx

# ===========================
# عرض الملف الشخصي
# ===========================
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'core/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

# ===========================
# تعديل الملف الشخصي
# ===========================
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', 'third_name',"fourth_name" , 'email', 'profile_image']

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'core/profile_edit.html'
    pk_url_kwarg = 'user_id'

    def get_success_url(self):
        return reverse_lazy('core:profile', kwargs={'user_id': self.object.id})
