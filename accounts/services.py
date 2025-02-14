from accounts.models import User
from django.db.models.query import QuerySet


class AccountService:
    def __init__(self) -> None:
        pass

    def get_user_role(self, user: User) -> User:
        user_role: User = User.objects.filter(
            id=user.id).first()

        return user_role

    def has_role(self, user, role: str) -> bool:
        user_role = self.get_user_role(user)
        return user_role is not None and user_role.role == role

    def is_doctor(self, user) -> bool:
        return self.has_role(user, User.ROLE.DOCTOR)

    def is_patient(self, user) -> bool:
        return self.has_role(user, User.ROLE.PATIENT)

    def get_users_with_same_role(self, role: str) -> QuerySet:
        return User.objects.filter(role=role)
