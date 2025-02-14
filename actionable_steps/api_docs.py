from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from actionable_steps.models import ActionableTask
from actionable_steps.serializers import ActionableTaskSerializer


ACTIONABLETASKSWAGGER_DOCS = swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            name='status',
            in_=openapi.IN_QUERY,
            description="Filter tasks by status (e.g., 'pending', 'completed').",
            type=openapi.TYPE_STRING,
            enum=ActionableTask.STATUS.ALL,
            default='pending'
        ),
        openapi.Parameter(
            name='type',
            in_=openapi.IN_QUERY,
            description="Filter tasks by type (e.g., 'checklist', 'plan').",
            type=openapi.TYPE_STRING,
            enum=ActionableTask.TASK_TYPE.ALL
        ),
        openapi.Parameter(
            name='start_date',
            in_=openapi.IN_QUERY,
            description="Filter tasks by start date (YYYY-MM-DD).",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE
        ),
        openapi.Parameter(
            name='end_date',
            in_=openapi.IN_QUERY,
            description="Filter tasks by end date (YYYY-MM-DD).",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_DATE
        ),
    ],
    responses={
        200: openapi.Response(
            description="List of active tasks",
            schema=ActionableTaskSerializer(many=True)
        ),
        400: openapi.Response(
            description="Invalid request parameters",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        ),
        403: openapi.Response(
            description="Permission denied",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    },
    operation_description="Retrieve active tasks for the authenticated user.\
        Tasks can be filtered by status, type, and date range."
)
