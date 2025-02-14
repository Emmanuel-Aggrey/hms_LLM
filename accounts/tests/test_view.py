from accounts.factories import UserFactory
from accounts.models import User
from django.urls import reverse
from rest_framework import status
from testing.base import BaseAPITest
from literals.factories import DeviceBrandFactory, DeviceTypeFactory
from user_roles.models import Role, UserRole


class UserProfileTest(BaseAPITest):
    def setUp(self):
        self.user: User = UserFactory()
        super().setUp()
        from repaire_request.factories import RepaireRequestFactory
        self.repaire_request = RepaireRequestFactory()
        self.client.force_authenticate(user=self.user)

    def test_deactivate_user(self):
        url = reverse('account:user-detail', kwargs={'pk': self.user.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_deactivate_user_permission(self):
        another_user = UserFactory()
        url = reverse('account:user-detail', kwargs={'pk': another_user.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user(self):
        url = reverse('account:user-list')

        data = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'password': 'securepassword123'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(username='new_user')
        self.assertEqual(new_user.email, 'new_user@example.com')

    def test_update_user(self):
        url = reverse('account:user-detail', kwargs={'pk': self.user.pk})

        updated_data = {
            'address': "testme233-Accra",
        }

        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()

        self.assertEqual(self.user.address, 'testme233-Accra')

    def test_create_repairer(self):
        url = reverse('account:repairers_create')
        self.user.set_role(Role.ROLES.REPAIRER)

        data = {
            'user': self.user.id,
            'skills': ['screen', 'charger'],

            "services_offered": [],
            "device_type": [DeviceTypeFactory().id],
            "device_brand": DeviceBrandFactory().id,
            "role": Role.ROLES.REPAIRER

        }

        response = self.client.post(url, data, format='json')

        user_role: UserRole = UserRole.objects.get(user=data.get('user'))
        self.assertEqual(user_role.role.name, Role.ROLES.REPAIRER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_repairer_invalid_user(self):
        url = reverse('account:repairers_create')
        self.user.set_role(Role.ROLES.CLIENT)

        data = {
            'user': UserFactory().id,
            'skills': ['screen', 'charger'],

            "services_offered": [],
            "device_type": DeviceTypeFactory().id,
            "device_brand": DeviceBrandFactory().id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
