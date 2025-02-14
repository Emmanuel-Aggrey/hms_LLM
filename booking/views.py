from rest_framework import viewsets
from doctorsnote.models import DoctorsNote
from rest_framework.permissions import IsAuthenticated
from booking.serializers import BookSerializer, BookDoctoreSerializer, CloseBookingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.models import User
from accounts.serializers import UserSerializer
from rest_framework.request import Request
from core.dependency_injection import service_locator
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


class BaseMixin:
    pass


class BookDoctorSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DoctorsNote.objects.order_by('id')
    serializer_class = BookSerializer

    @swagger_auto_schema(
        operation_description="Book a doctor for a patient",
        responses={201: UserSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='available-doctors')
    def available_doctors(self, request: Request):
        is_patient = service_locator.account_service.is_patient(request.user)

        if not is_patient:
            raise PermissionDenied()

        doctors = service_locator.account_service.get_users_with_same_role(
            User.ROLE.DOCTOR).filter(is_available=True)

        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Book a doctor for a patient",
        request_body=BookDoctoreSerializer,
        responses={201: BookSerializer}
    )
    @action(detail=False, methods=['post'], url_path='book-a-doctor', serializer_class=BookDoctoreSerializer)
    def book_doctor(self, request: Request):
        is_patient = service_locator.account_service.is_patient(request.user)
        doctor = get_object_or_404(User, id=request.data.get('doctor'))

        if not is_patient:
            raise PermissionDenied()

        doctors_note = service_locator.booking_service.book_doctor(
            user=request.user, doctor=doctor)
        serializer = BookSerializer(doctors_note)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my-patients', serializer_class=BookSerializer)
    def my_patients(self, request: Request):
        is_patient = service_locator.account_service.is_patient(request.user)

        if is_patient:
            raise PermissionDenied()

        doctors = service_locator.booking_service.my_patients(
            doctor=request.user)

        serializer = BookSerializer(doctors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Close Booking",
        request_body=CloseBookingSerializer,
        responses={200: BookSerializer}
    )
    @action(detail=False, methods=['post'], url_path='close-booking')
    def close_booking(self, request: Request, *args, **kwargs):
        booking_id = request.data.get('booking_id')
        booking = service_locator.booking_service.close_booking(booking_id)
        serializer = BookSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)
