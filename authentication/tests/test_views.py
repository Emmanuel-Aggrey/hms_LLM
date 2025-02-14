
from accounts.factories import UserFactory, User
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from testing.base import BaseAPITest
from django.utils import timezone
from datetime import timedelta


class UserProfileTest(BaseAPITest):
    def setUp(self):
        self.user: User = UserFactory()
        super().setUp()

    def test_signup_user(self):
        url = reverse("authentication:user-signup")
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "testpassword123",
        }

        res: Response = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data, 'kindly check your email to verify your account')

    def test_login_with_jwt(self):
        url = reverse("authentication:user-signup")
        data = {
            "email": "loginuser@example.com",
            "first_name": "Login",
            "last_name": "User",
            "password": "testpassword123",
        }
        signup_res = self.client.post(url, data)

        self.assertEqual(signup_res.status_code, status.HTTP_201_CREATED)

        login_url = reverse("authentication:email_password")
        res = self.client.post(login_url, {
            "email": "loginuser@example.com",
            "password": "testpassword123",
        })

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data, "User account is not active")

    def test_otp_login_with_expired_token(self):
        token = "123456"
        self.user.set_token(token)
        self.user.expire_at = timezone.now() - timedelta(days=1)
        self.user.save()

        url = reverse("authentication:verified_otp")
        res = self.client.post(url, {"token": token})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_email(self):
        url = reverse("authentication:user-signup")
        data = {
            "email": "resetuser@example.com",
            "first_name": "Reset",
            "last_name": "User",
            "password": "testpassword123",
        }
        self.client.post(url, data)

        reset_url = reverse("authentication:login_email")
        reset_data = {
            "email": "resetuser@example.com"
        }
        res: Response = self.client.post(reset_url, reset_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, "Verification code sent")

    def test_password_reset_mobile(self):
        url = reverse("authentication:user-signup")
        data = {
            "email": "resetuser@example.com",
            "first_name": "Reset",
            "last_name": "User",
            "password": "testpassword123",
        }
        self.client.post(url, data)
        self.user.mobile = "123456791"
        self.user.save()

        reset_url = reverse("authentication:login_mobile")
        reset_data = {
            "mobile": self.user.mobile
        }
        res: Response = self.client.post(reset_url, reset_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, "Verification code sent")

    def test_forgot_password(self):
        url = reverse("authentication:forgot_password")
        data = {
            "email": self.user.email
        }

        res: Response = self.client.post(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, "Password reset link sent. Please check your email.")

    def test_change_password(self):
        user = User.objects.create_user(
            email="changepassworduser@example.com",
            password="oldpassword"
        )
        url = reverse('authentication:change_password')
        data = {
            "password": "newpassword@123",
            "password2": "newpassword@123"
        }

        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Password changed successfully.")

    def test_invalid_login(self):
        url = reverse('authentication:email_password')
        data = {
            "email": "invaliduser@example.com",
            "password": "wrongpassword"
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, 'Email or Password is not valid')
