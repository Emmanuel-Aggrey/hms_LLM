from django.db import models
from accounts.models import User
from core.models import BaseModel


class BookDoctor(BaseModel):
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+")
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+")
    is_active = models.BooleanField(default=True)
