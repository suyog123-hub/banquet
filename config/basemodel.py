import uuid
from django.db import models
from django.conf import settings
class Base(models.Model):
    reference_id = models.UUIDField(unique=True, null=False, default=uuid.uuid4, editable=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+',
                                   null=True, blank=False, db_column='created_by')
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='+',
                                   null=True, db_column='updated_by')
    updated_at = models.DateTimeField(auto_now=True)

    is_delete = models.BooleanField(default=False)
    class Meta:
        abstract = True     

