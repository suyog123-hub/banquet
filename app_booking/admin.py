# admin.py
from django.contrib import admin
from .models import Bookingmodel


@admin.register(Bookingmodel)
class BookingmodelAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'name',
        'booking_time',
        'contact',
        'Events',
        'Booking_stauts',
        'number_of_guest',
        'email',
        'payment_type',
    ]
    
