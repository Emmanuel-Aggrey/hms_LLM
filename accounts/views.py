from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from accounts.serializers import UserSerializer, UserAvailabilitySerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class UserSerializerView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.order_by('role')
    serializer_class = UserSerializer


class UserAvailabilitySerializer(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserAvailabilitySerializer

    def create(self, request, *args, **kwargs):
        availability_status = request.data.get('is_available', False)

        try:
            user: User = User.objects.get(pk=self.request.user.pk)
            user.is_available = availability_status
            user.save(update_fields=['is_available'])
            return Response({'status': 'availability updated'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
