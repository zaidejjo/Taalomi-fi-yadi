from django.http import HttpResponseForbidden
from functools import wraps

def role_required(allowed_roles=[]):
    """
    يحدد أي دور يمكنه الوصول للـ view
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("يجب تسجيل الدخول للوصول لهذه الصفحة")
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("ليس لديك الصلاحية للوصول لهذه الصفحة")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
