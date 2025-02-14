from accounts.models import User
from doctorsnote.models import DoctorsNote
import uuid
from django.core.exceptions import PermissionDenied


class DoctorNoteService:
    def __init__(self):
        pass

    def submit_note(self, doctor: User,  note: str, booking_id: uuid.UUID) -> DoctorsNote:

        create_note = DoctorsNote(
            booking_id=booking_id,
            note=note,
            created_by=doctor

        )
        create_note.save()
        return create_note

    def my_notes(self, user: User,  role: User.ROLE) -> DoctorsNote:
        from core.dependency_injection import service_locator

        if role == User.ROLE.DOCTOR:
            is_doctor = service_locator.account_service.is_doctor(user)
            if not is_doctor:
                raise PermissionDenied()
            return DoctorsNote.objects.filter(created_by=user)

        if role == User.ROLE.PATIENT:
            is_patient = service_locator.account_service.is_patient(user)

            if not is_patient:

                raise PermissionDenied()
            return DoctorsNote.objects.filter(booking__created_by=user)

        return DoctorsNote.objects.none()
