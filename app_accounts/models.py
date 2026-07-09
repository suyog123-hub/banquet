from django.db import models
from django.contrib.auth.models import AbstractUser
from config.basemodel import Base
from app_core.models import WeddingPalace
from django.contrib.auth.base_user import BaseUserManager



class User(AbstractUser, Base):
    email = models.EmailField(unique=True)   
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    organization = models.ForeignKey(
        WeddingPalace,
        on_delete=models.CASCADE,
        related_name="staff",
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=[
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("user", "User"),
    ], default="user")
    

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role"]

    def __str__(self):
        return self.username
    