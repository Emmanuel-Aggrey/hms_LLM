from rest_framework import serializers
from doctorsnote.models import DoctorsNote
from core.serializers import CreatedByMixin, BaseToRepresentation


class DoctorsNoteSerializer(CreatedByMixin, BaseToRepresentation, serializers.ModelSerializer):

    class Meta:
        model = DoctorsNote
        exclude = ['is_deleted']
        read_only_fields = ['id', 'created_by']

        extra_kwargs = {
            "booking": {"required": True}
        }

    def to_representation(self, instance: DoctorsNote):
        representation = super().to_representation(instance)

        representation['note'] = instance.decrypt_note

        return representation


class BookDoctorerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorsNote
        fields = ['doctor', 'note']
