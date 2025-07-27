import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import make_password
from users.models import User, ADMIN, USER
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory

pytestmark = pytest.mark.django_db


# Фикстуры
@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def regular_user():
    user = User(
        email="user@test.com",
        first_name="Test",
        last_name="User",
        phone="+1234567890",
        role=USER,
        is_active=True,
    )
    user.password = make_password("testpass123")
    user.save()
    return user


@pytest.fixture
def admin_user():
    user = User(
        email="admin@test.com",
        first_name="Admin",
        last_name="User",
        phone="+1234567890",
        role=ADMIN,
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )
    user.password = make_password("adminpass123")
    user.save()
    return user


# Тесты моделей
class TestUserModel:
    def test_user_creation(self, regular_user):
        assert regular_user.email == "user@test.com"
        assert regular_user.role == USER
        assert regular_user.check_password("testpass123")
        assert not regular_user.is_staff

    def test_admin_creation(self, admin_user):
        assert admin_user.email == "admin@test.com"
        assert admin_user.role == ADMIN
        assert admin_user.check_password("adminpass123")
        assert admin_user.is_staff


# Тесты API
class TestUserAPI:
    def test_user_registration(self, api_client):
        url = reverse("user-register")
        data = {
            "email": "newuser@test.com",
            "password": "newpass123",
            "first_name": "New",
            "last_name": "User",
            "phone": "+1234567890",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@test.com").exists()

    def test_user_login(self, api_client, regular_user):
        url = reverse("token-obtain")
        data = {"email": "user@test.com", "password": "testpass123"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_invalid_login(self, api_client, regular_user):
        url = reverse("token-obtain")
        data = {"email": "user@test.com", "password": "wrongpassword"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh(self, api_client, regular_user):
        refresh = RefreshToken.for_user(regular_user)
        url = reverse("token-refresh")
        data = {"refresh": str(refresh)}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


class TestPasswordReset:
    def test_password_reset_request(self, api_client, regular_user, mailoutbox):
        url = reverse("reset-password")
        data = {"email": "user@test.com"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert len(mailoutbox) == 1
        assert mailoutbox[0].subject == "Сброс пароля"

    def test_password_reset_confirm(self, api_client, regular_user):
        # Сначала получаем токен сброса
        from django_rest_passwordreset.models import ResetPasswordToken

        token = ResetPasswordToken.objects.create(user=regular_user)

        url = reverse("reset-password-confirm")
        data = {"token": token.key, "password": "newpassword123"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        regular_user.refresh_from_db()
        assert regular_user.check_password("newpassword123")


class TestUserPermissions:
    def test_admin_access(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("user-register")
        data = {
            "email": "admin_created@test.com",
            "password": "testpass123",
            "first_name": "Admin",
            "last_name": "Created",
            "phone": "+1234567890",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_admin_can_change_user_role(self, api_client, admin_user, regular_user):
        """Администратор может изменять роль пользователя"""
        api_client.force_authenticate(user=admin_user)
        factory = RequestFactory()
        request = factory.get("/")
        request.user = admin_user

        regular_user.role = ADMIN
        regular_user.save(request=request)
        updated_user = User.objects.get(pk=regular_user.pk)
        assert updated_user.role == ADMIN

    def test_regular_user_cant_change_role(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        regular_user.role = ADMIN
        with pytest.raises(PermissionDenied):
            regular_user.save()
