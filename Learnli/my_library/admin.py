from django.contrib import admin
from .models  import Reaction,Content,Ebook,Section,Sub_Section,Reviews,Book_Payment

# Register your models here.
admin.site.register(Reaction)
admin.site.register(Content)
admin.site.register(Ebook)
admin.site.register(Section)
admin.site.register(Sub_Section)
admin.site.register(Reviews)
admin.site.register(Book_Payment)
