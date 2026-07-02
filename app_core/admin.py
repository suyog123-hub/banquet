# admin.py
from django.contrib import admin
from .models import WeddingPalace

@admin.register(WeddingPalace)
class WeddingPalaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'capacity', 'base_price', 'is_available', 'created_at']
    list_filter = ['city', 'is_available']
    search_fields = ['name', 'city', 'address']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
