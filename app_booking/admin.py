# app_booking/admin.py

from django.contrib import admin
from .models import Bookingmodel

@admin.register(Bookingmodel)
class BookingmodelAdmin(admin.ModelAdmin):
    list_display = [
       'reference_id',         
        'user',
        'name',
        'booking_time',
        'event',
        'booking_status',
        'number_of_guest',
        'payment_type',
        'created_at'
    ]
    
    list_display_links = ['reference_id'] 

    search_fields = [
        'reference_id',        
        'user__username',
        'user__email',
        'name',
        'email',
        'contact'
    ]

    readonly_fields = ['reference_id', 'created_at', 'updated_at']

    list_filter = [
        'event',
        'booking_status',
        'payment_type',
        'booking_time'
    ]
    
    ordering = ['-created_at']