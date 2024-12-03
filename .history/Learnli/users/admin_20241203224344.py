from django.contrib import admin
from .models import user_Profile
from .models import FlaggedContent
from django.utils.html import format_html

# Register your models here.
admin.site.register(user_Profile)
@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('content_object','id', 'content_category', 'reported_by', 'reason', 'date_reported', 'reviewed', 'approved')
    list_filter = ('content_type', 'reviewed', 'approved')
    search_fields = ('reason', 'reported_by__username')


