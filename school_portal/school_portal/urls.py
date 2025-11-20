from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from core.views import SignUpView
from django.conf import settings
from django.conf.urls.static import static

# Sitemaps
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import CoreSitemap
from academics.sitemaps import AcademicsSitemap
from assignments.sitemaps import AssignmentsSitemap
from attendance.sitemaps import AttendanceSitemap
from competitions.sitemaps import CompetitionsSitemap
from ai_chat.sitemaps import AIChatSitemap

sitemaps = {
    'core': CoreSitemap(),
    'academics': AcademicsSitemap(),
    'assignments': AssignmentsSitemap(),
    'attendance': AttendanceSitemap(),
    'competitions': CompetitionsSitemap(),
    'ai_chat': AIChatSitemap(),
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('core/', include('core.urls')),
    path('academics/', include('academics.urls')),
    path('attendance/', include('attendance.urls')),
    path('assignments/', include('assignments.urls')),
    path('competitions/', include('competitions.urls')),
    path('chat/', include(('ai_chat.urls', 'ai_chat'), namespace='ai_chat')),

    # Accounts
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/core/'), name='logout'),

    # Password Reset
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Sitemap
    path('sitemap.xml', RedirectView.as_view(url='/static/sitemap.xml')),

    # Robots
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # Home redirect
    path('', RedirectView.as_view(url='/core/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
