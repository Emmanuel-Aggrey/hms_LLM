from accounts.models import User
from .models import BookDoctor
from typing import List
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class BookingService:
    def __init__(self):
        pass

    def book_doctor(self, user: User, doctor: User) -> BookDoctor:
        from core.dependency_injection import service_locator

        if service_locator.account_service.is_doctor(doctor):

            raise ValidationError(
                detail={"detail": "Only patients can book a doctor."},
                code="invalid_request"
            )

        existing_booking = BookDoctor.objects.filter(
            patient=user, doctor=doctor, is_active=True).first()

        if existing_booking:
            raise ValidationError(
                code="invalid_booking",
                detail={"detail": "you have already booked this doctor."}
            )

        if not doctor.is_available:
            raise ValidationError(
                detail={"detail": "sorry, this doctor is not available"},
                code="invalid_request")

        booking = BookDoctor(
            patient=user,
            doctor=doctor,
            is_active=True,
        )

        booking.save()
        return booking

    def my_patients(self, doctor: User) -> List[BookDoctor]:
        from core.dependency_injection import service_locator

        if service_locator.account_service.is_patient(doctor):
            raise ValidationError(detail={"detail": "Only doctors can have patients booked with them."},
                                  code='invalid_request')

        booked_patients = BookDoctor.objects.filter(
            doctor=doctor).select_related('patient')
        return booked_patients

    def close_booking(self, booking_id):
        booking = get_object_or_404(BookDoctor, id=booking_id)
        booking.is_active = False
        booking.save(update_fields=['is_active'])
        return booking
