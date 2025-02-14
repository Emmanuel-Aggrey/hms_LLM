import uuid

from django.db import models


class OBJECT_TYPE:

    PAYMENT = "payment"
    REPAIR_MANAGEMNT = "repair_managemnt"
    SUPPORT = "support"
    ACCOUNT = "account"

    ALL = (
        PAYMENT,
        REPAIR_MANAGEMNT,
        SUPPORT,
        ACCOUNT


    )
    CHOICES = (
        (PAYMENT, ("Payment")),
        (REPAIR_MANAGEMNT, ("Repaire Managemnt")),
        (SUPPORT, ("SUPPORT")),
        (ACCOUNT, ("ACCOUNT")),


    )


class BaseModel(models.Model):
    OBJECT_TYPE = OBJECT_TYPE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
