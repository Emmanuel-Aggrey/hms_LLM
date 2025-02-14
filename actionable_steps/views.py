from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from actionable_steps.models import ActionableTask
from actionable_steps.serializers import ActionableTaskSerializer, MarkActionableTaskAsCompletedSerializer
import logging
from core.dependency_injection import service_locator
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from actionable_steps.api_docs import ACTIONABLETASKSWAGGER_DOCS
logger = logging.getLogger(__name__)


class ActionableTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ActionableTaskSerializer
    queryset = ActionableTask.objects.order_by('-created_at')

    @ACTIONABLETASKSWAGGER_DOCS
    @action(detail=False, methods=['get'], url_path='active-tasks')
    def active_tasks(self, request: Request):
        user = request.user
        status_filter = request.query_params.get(
            'status', ActionableTask.STATUS.PENDING)
        task_type_filter = request.query_params.get('type', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        tasks = ActionableTask.objects.none()
        if service_locator.account_service.is_patient(user):
            tasks = ActionableTask.objects.filter(patient=user)
        elif service_locator.account_service.is_doctor(user):
            tasks = ActionableTask.objects.filter(doctor=user)

        filters = {}
        if status_filter:
            filters['status'] = status_filter
        if task_type_filter:
            filters['task_type'] = task_type_filter
        if start_date and end_date:
            filters['scheduled_date__range'] = [start_date, end_date]

        tasks = tasks.filter(**filters)
        serializer = ActionableTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Book a doctor for a patient",
        request_body=MarkActionableTaskAsCompletedSerializer,
        responses={200: ActionableTaskSerializer()}
    )
    @action(detail=False, methods=['post'], url_path='mark-as-completed')
    def mark_as_completed(self, request: Request, pk=None):

        task_id = request.data.get('task_id', None)
        task = get_object_or_404(
            ActionableTask, id=task_id)

        task = service_locator.actionable_steps_service.process_task_completion(
            task.id, request.user.id)
        serializer = ActionableTaskSerializer(task)
        return Response(serializer.data)
