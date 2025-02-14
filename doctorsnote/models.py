from django.db import models
from accounts.models import User
from django.core import signing
from core.models import BaseModel
from booking.models import BookDoctor


class DoctorsNote(BaseModel):

    booking = models.ForeignKey(
        BookDoctor, on_delete=models.CASCADE, null=True)
    note = models.TextField(null=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+")

    def save(self, *args, **kwargs):

        if not self.is_encrypted(self.note):
            self.note = signing.dumps(self.note, compress=True)
        super().save(*args, **kwargs)

    @property
    def decrypt_note(self):
        return signing.loads(self.note)

    def is_encrypted(self, note):
        try:
            signing.loads(note)
            return True
        except signing.BadSignature:
            return False
