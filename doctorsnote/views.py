from rest_framework import viewsets
from doctorsnote.models import DoctorsNote
from rest_framework.permissions import IsAuthenticated
from doctorsnote.serializers import DoctorsNoteSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from core.dependency_injection import service_locator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from accounts.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from booking.models import BookDoctor


class BaseMixin:
    pass


class DoctorsNoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DoctorsNote.objects.order_by('id')
    serializer_class = DoctorsNoteSerializer

    @swagger_auto_schema(
        operation_description="Book a doctor for a patient",
        request_body=DoctorsNoteSerializer,
        responses={201: DoctorsNoteSerializer}
    )
    @action(detail=False, methods=['post'], url_path='submit-note', serializer_class=DoctorsNoteSerializer)
    def submit_note(self, request: Request):
        booking_id = request.data.get('booking', None)

        get_object_or_404(BookDoctor, id=booking_id)
        note = request.data.get('note', None)

        is_doctor = service_locator.account_service.is_doctor(request.user)
        if not is_doctor:
            raise PermissionDenied()

        doctors_note = service_locator.doctor_note_service.submit_note(
            doctor=request.user, booking_id=booking_id, note=note
        )

        # Extract actionable steps from the note using the LLM
        actionable_steps = service_locator.actionable_steps_service.extract_actionable_steps(
            doctors_note.decrypt_note)

        patient = doctors_note.booking.patient
        doctor = request.user

        service_locator.actionable_steps_service.create_tasks_from_llm_output(
            llm_output=actionable_steps,
            patient=patient,
            doctor=doctor,
            note_id=doctors_note.id
        )

        serializer = DoctorsNoteSerializer(doctors_note)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="my notes",

        manual_parameters=[

            openapi.Parameter(
                "role",
                openapi.IN_QUERY,
                description="user role",
                enum=list(User.ROLE.ALL),
                type=openapi.TYPE_STRING,
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path='my-notes')
    def my_notes(self, request: Request):

        role = request.query_params.get('role', None)

        doctors_note = service_locator.doctor_note_service.my_notes(
            user=request.user, role=role)

        serializer = DoctorsNoteSerializer(doctors_note, many=True)
        return Response(serializer.data)
