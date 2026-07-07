from django.db import models
from django.conf import settings 
from config.basemodel import Base

class Bookingmodel(Base):
    EVENTS_CHOICE = [
        ("wedding", "Wedding"),
        ("birthday", "Birthday"),
        ("ceremony", "Ceremony"),
        ("others", "Others"),
    ]
    
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    PAYMENT_TYPE = [
        ("cash", "Cash"),
        ("esewa", "Esewa"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    name = models.CharField(max_length=60, blank=True)
    booking_time = models.DateField()
    contact = models.CharField(max_length=15)  
    event = models.CharField(choices=EVENTS_CHOICE, null=True, default="wedding") 
    booking_status = models.CharField(choices=BOOKING_STATUS, null=True, default='pending') 
    number_of_guest = models.IntegerField()
    email = models.EmailField(blank=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, null=True, default='cash')
    details = models.TextField()

    class Meta:
        db_table = 'Booking'
        unique_together = ['booking_time']  
        ordering = ['-booking_time']  

    def __str__(self):
        return f"{self.user.username} - {self.booking_time}"