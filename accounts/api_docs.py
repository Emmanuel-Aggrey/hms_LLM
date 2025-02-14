from accounts.serializers import AssignRoleResponseSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

PASSWORD_RESET_SWAGGER_DOCS = swagger_auto_schema(
    operation_description="Password Reset",
    responses={},
    manual_parameters=[
        openapi.Parameter(
            "uid",
            openapi.IN_QUERY,
            description="uid",
            type=openapi.TYPE_STRING,

        ),
        openapi.Parameter(
            "token",
            openapi.IN_QUERY,
            description="token",
            type=openapi.TYPE_STRING,
        ),
    ],
)


AssignRoleResponse_API_DOC = swagger_auto_schema(
    responses={200: AssignRoleResponseSerializer}
)
