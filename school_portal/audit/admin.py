from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'entity', 'entity_id')
    list_filter = ('action', 'entity')
    search_fields = ('actor__username', 'details')
