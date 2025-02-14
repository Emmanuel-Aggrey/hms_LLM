
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (

    SimpleUserAccountSerializer,

    UserAccountSerializer,
    UserLoginSerializer,
)


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    if not user.is_active:
        return Response(
            data="User account is not active", status=status.HTTP_401_UNAUTHORIZED
        )
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class UserSignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserAccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        user: User = serializer.save()
        user.set_password(password)
        user.save()

        return Response(
            data=SimpleUserAccountSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class EmailPasswordLoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        role = serializer.validated_data.get("role")

        user: User = authenticate(email=email, password=password)
        existing_user: User = User.objects.filter(
            email=email, role=role).first()

        if existing_user and existing_user.is_active:

            return Response(
                {"token": get_tokens_for_user(
                    user), "user": SimpleUserAccountSerializer(user).data},
                status=status.HTTP_200_OK,
            )

        if existing_user and not existing_user.is_active:
            return Response(
                "User account is not active", status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            "Email or Password is not valid", status=status.HTTP_401_UNAUTHORIZED
        )
