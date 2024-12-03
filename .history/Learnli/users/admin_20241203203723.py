from django.contrib import admin
from .models import user_Profile
from .models import FlaggedContent

# Register your models here.
admin.site.register(user_Profile)


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'reported_by', 'reason', 'date_reported', 'is_resolved')
    list_filter = ('reason', 'date_reported', 'is_resolved')
    search_fields = ('content_object', 'reported_by__username', 'reason')
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
        self.message_user(request, "Selected flagged content marked as resolved.")
    mark_as_resolved.short_description = "Mark selected content as resolved"
 