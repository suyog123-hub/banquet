# models.py
from django.db import models
from django.utils.text import slugify
from config.basemodel import Base
class WeddingPalace(Base):

    CURRENCY_CHOICES = [
        ('NPR', 'NPR (Nepalese Rupee)'),
        ('USD', 'USD (US Dollar)'),
        ('INR', 'INR (Indian Rupee)'),
    ]
    name = models.CharField(max_length=200, help_text="Name of the wedding palace")
    slug = models.SlugField(max_length=220, unique=True, blank=True, help_text="Auto-generated from name")
    address = models.TextField(help_text="Full address")
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Nepal')
    location = models.URLField(help_text="please provide the url of the google map  ")
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    

    capacity = models.PositiveIntegerField(help_text="Maximum number of guests")
    parking_capacity = models.PositiveIntegerField(blank=True, null=True)

    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NPR')
    is_available = models.BooleanField(default=True)

    description = models.TextField(help_text="Overview and highlights")
    cover_image = models.ImageField(upload_to='palace_covers/',blank=True,null=True,help_text="Main/cover image of the palace") 
    video = models.FileField(upload_to='palace_video/',blank=True,null=True,help_text="Main video of your palace") 
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Wedding Palace"
        verbose_name_plural = "Wedding Palaces"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'organization info'