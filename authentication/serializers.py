from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db import transaction


class UserAccountSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions',
                   'last_login', 'date_joined', 'username']

        read_only_fields = ["id", "is_superuser", 'is_staff']
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True, "required": True},
            "is_superuser": {"read_only": True},
            "role": {"required": True},


        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = self.initial_data.get("password_2")

        if password and password2:
            if password != password2:
                raise serializers.ValidationError(
                    code="password2",
                    detail="Password and Confirm Password do not match"
                )

        validate_password(password)
        return super().validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        validated_data['username'] = validated_data.get(
            'email', validated_data.get('mobile'))

        validated_data.pop('password2', None)
        user: User = User.objects.create(**validated_data)

        return user


class SimpleUserAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_available",
            "role",
        ]


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password", 'role']

        extra_kwargs = {

            "role": {"required": True},


        }
