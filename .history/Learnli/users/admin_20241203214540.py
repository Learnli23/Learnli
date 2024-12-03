from django.contrib import admin
from .models import user_Profile
from .models import FlaggedContent
from django.utils.html import format_html

# Register your models here.
admin.site.register(user_Profile)


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'reason', 'reported_by', 'date_reported','is_approved_status',
                    'is_reviewed_status')
    list_filter = ('content_type', 'date_reported')
    search_fields = ('reason', 'reported_by__username')
    readonly_fields = ('content_type', 'object_id', 'reported_by', 'date_reported')

    def content_object(self, obj):
        return obj.content_object
    content_object.short_description = 'Flagged Content'

    def is_approved_status(self, obj):
        if obj.approved:
            return format_html('<span style="color: green;">&#10004;</span>')  # Green check mark for approved
        else:
            return format_html('<span style="color: red;">&#10006;</span>')  # Red cross mark for not approved
    is_approved_status.short_description = 'Approval Status'

    def is_reviewed_status(self, obj):
        if obj.reviewed:
            return format_html('<span style="color: green;">&#10004;</span>')  # Green check mark for reviewede
        else:
            return format_html('<span style="color: red;">&#10006;</span>')  # Red cross mark for not reviewed
    is_reviewed_status.short_description = 'review Status'
