from django.db import models

# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.TextField()
    message = models.TextField()

    class Meta:
        db_table = 'contact'
       