from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden

class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        return HttpResponseForbidden("ليس لديك الصلاحية للوصول لهذه الصفحة")
