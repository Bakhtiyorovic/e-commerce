from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(BlogPost)
admin.site.register(Product)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'image')
    search_fields = ('title', 'date')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)