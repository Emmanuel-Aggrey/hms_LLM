from rest_framework import serializers
from actionable_steps.models import ActionableTask


class ActionableTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionableTask
        exclude = ['is_deleted']


class MarkActionableTaskAsCompletedSerializer(serializers.ModelSerializer):
    task_id = serializers.UUIDField(source="id")

    class Meta:
        model = ActionableTask
        fields = ['task_id']
