from accounts.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions',
                   'last_login', 'date_joined', 'username', 'is_superuser', 'is_staff']

        read_only_fields = ['date_joined', 'id']


class UserAvailabilitySerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = ['is_available']
