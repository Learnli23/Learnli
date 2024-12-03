from django.contrib import admin
from .models import user_Profile
from .models import FlaggedContent

# Register your models here.
admin.site.register(user_Profile)


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object','reported_by', 'reason', 'date_reported' )
    list_filter = ('content_type', 'reviewed', 'approved')
    search_fields = ( 'reason', 'reported_by__username')
    
 