from django.contrib import admin
from .models import user_Profile
from .models import FlaggedContent

# Register your models here.
admin.site.register(user_Profile)


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('content_type','object_id','reported_by', 'date_reported', 'reason' )
    list_filter = ('content_type', 'reviewed', 'approved')
    search_fields = ( 'reason', 'date_reported','reported_by__username')
    readonly_fields = ( 'content_type', 'object_id', 'content_type','reported_by','date_reported')
    
 