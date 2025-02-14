from accounts.factories import UserFactory
from testing.base import BaseAPITest

from .dependency_injection import service_locator


class CoreServiceTestCase(BaseAPITest):
    def setUp(self):
        self.user = UserFactory()
        super().setUp()

        self.client.force_authenticate(user=self.user)

    # @skip("SendGrid Testing mode")
    def test_send_email(self):

        service_locator.core_service.send_email(
            template_path="company_invite.html",
            template_context={},
            to_emails=["sageliteoff@gmail.com"],
            subject="Company Invite",
        )
