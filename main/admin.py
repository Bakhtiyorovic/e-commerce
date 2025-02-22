from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'image')
    search_fields = ('title', 'date')

