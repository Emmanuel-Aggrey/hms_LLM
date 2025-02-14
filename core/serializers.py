from rest_framework import serializers


class CreatedByMixin:
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user

        return super().create(validated_data)


class AbstractSerializer(serializers.ModelSerializer):

    class Meta:
        model = None
        fields = "__all__"
        depth = 1


class BaseToRepresentation:
    def to_representation(self, instance):
        original_fields = dict(self.fields)

        base_serializer = AbstractSerializer(instance=instance)
        base_serializer.Meta.model = instance.__class__
        data = base_serializer.data if instance else {}

        user_sensitive_fields = ['password',
                                 'is_superuser', 'groups', 'user_permissions']
        for key, value in data.items():
            if isinstance(value, dict):
                for field in user_sensitive_fields:
                    value.pop(field, None)

        # Add custom fields
        for field_name, field in original_fields.items():
            if field_name not in data:
                if isinstance(field, serializers.SerializerMethodField):
                    method_name = f'get_{field_name}'
                    data[field_name] = getattr(self, method_name)(instance)
                else:
                    value = getattr(instance, field_name, None)
                    data[field_name] = field.to_representation(
                        value) if value is not None else None

        return data
