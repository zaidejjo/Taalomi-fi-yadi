# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "second_name", "third_name", "fourth_name", "password1", "password2", "role", "grade", "section")

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        # رقم وديجتس فقط وطول 10 بالضبط
        if not re.fullmatch(r"\d{10}", username):
            raise ValidationError("الرقم الوطني يجب أن يتكوّن من 10 أرقام بالضبط (أرقام فقط).")
        # يمكن إضافة تحقق من التكرار إذا أردت:
        if User.objects.filter(username=username).exists():
            raise ValidationError("هذا الرقم الوطني مستخدم مسبقًا.")
        return username

    def clean_password2(self):
        # تأكد من أن كلمة المرور تلبي مدققات Django الافتراضية
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("كلمتا المرور غير متطابقتين.")
        # استخدم مدقق كلمة المرور الافتراضي (طول، تعقيد حسب settings)
        try:
            password_validation.validate_password(password2, self.instance)
        except ValidationError as e:
            raise ValidationError(e.messages)
        return password2
