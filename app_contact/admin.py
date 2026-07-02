from .models import contact
from django.contrib import admin

@admin.register(contact)
class contactAdmin(admin.ModelAdmin):
    list_display=['name','email','message','phone']
