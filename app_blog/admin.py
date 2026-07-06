from django.contrib import admin
from .models import Content ,BlogCategory
# Register your models here.

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display=["title"]


@admin.register(Content)
class BlogSubCategoryAdmin(admin.ModelAdmin):
    list_display=["heading","date","image","content"]
