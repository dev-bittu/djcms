from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "likes", "published_on", "creator", "is_active"]
    fields = ["title", "desc", "content", "categories", "thumbnail"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["comment", "blog", "likes", "published_on", "is_active"]
    fields = ["comment", "blog"]
