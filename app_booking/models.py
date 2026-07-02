from django.db import models
# Create your models here.

class Bookingmodel(models.Model):
    EVENTS_CHOICE = [
        ("wedding","wedding"),
        ("Birthday","Birthday"),
        ("Ceremony","Ceremony"),
       ( "Otheres","Others"),
    ]
    BOOKING_STATUS =[
        ('pending','pending'),
        ('accepted','accepted'),
        ('cancelled','cancelled'),
        ('completed','completed'),
    ]
    PAYMENT_TYPE = [
        ("cash","cash"),
        ("esewa","esewa"),
    ]
    name = models.CharField(max_length= 60)
    booking_time = models.DateField()
    contact = models.IntegerField()
    Events = models.CharField( choices=EVENTS_CHOICE , null=True , default="wedding")
    Booking_stauts = models.CharField(choices=BOOKING_STATUS , null= True , default='pending')
    number_of_guest = models.IntegerField()
    email= models.EmailField()
    payment_type = models.CharField(choices=PAYMENT_TYPE, null=True , default='cash')
    details = models.TextField()

    class Meta:
        db_table = 'Booking'
        unique_together = ['booking_time']
      
