from django.contrib import admin
from .models import user_Profile
from .models import FlaggedContent

# Register your models here.
admin.site.register(user_Profile)


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'reason', 'reported_by', 'date_reported')
    list_filter = ('content_type', 'date_reported')
    search_fields = ('reason', 'reported_by__username')
    readonly_fields = ('content_type', 'object_id', 'reported_by', 'date_reported')

    def content_object(self, obj):
        return obj.content_object
    content_object.short_description = 'Flagged Content'



    
 