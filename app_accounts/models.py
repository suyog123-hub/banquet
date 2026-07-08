from django.db import models
from django.contrib.auth.models import AbstractUser
from config.basemodel import Base
from app_core.models import WeddingPalace
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a normal user with role 'user'.
        """
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", "user")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, creator, username, email=None, password=None, **extra_fields):
        """
        Create and return an admin user.
        Only superusers can create admins.
        """
        if not creator.is_superuser:
            raise ValueError("Only superusers can create admins")

        email = self.normalize_email(email)
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("created_by", creator)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_staff(self, creator, username, email=None, password=None, **extra_fields):
        """
        Create and return a staff user.
        Only superusers can create staff.
        """
        if not creator.is_superuser:
            raise ValueError("Only superusers can create staff")

        email = self.normalize_email(email)
        extra_fields.setdefault("role", "staff")
        extra_fields.setdefault("created_by", creator)
        extra_fields.setdefault("is_staff", True)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user



class User(AbstractUser, Base):
    email = models.EmailField(unique=True)   # make email unique
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
    
    objects=UserManager()

    def __str__(self):
        return self.username
    
