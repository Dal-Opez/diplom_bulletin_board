import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from advertisements.models import Advertisement
from users.models import USER, ADMIN

User = get_user_model()


@pytest.fixture
def api_client():
    """Фикстура для API клиента"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def regular_user():
    """Фикстура для создания обычного пользователя"""
    user = User(
        email="user@test.com",
        first_name="Test",
        last_name="User",
        phone="+1234567890",
        role=USER,
        is_active=True
    )
    user.password = make_password("testpass123")
    user.save()

    # Проверка корректности создания пользователя
    assert user.pk is not None
    assert user.check_password("testpass123")
    assert user.role == USER
    assert user.is_active
    return user


@pytest.fixture
def admin_user():
    """Фикстура для создания администратора"""
    user = User(
        email="admin@test.com",
        first_name="Admin",
        last_name="User",
        phone="+1234567890",
        role=ADMIN,
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    user.password = make_password("adminpass123")
    user.save()

    # Проверка корректности создания админа
    assert user.pk is not None
    assert user.check_password("adminpass123")
    assert user.role == ADMIN
    assert user.is_staff
    assert user.is_superuser
    return user


@pytest.fixture
def second_user():
    """Фикстура для создания второго пользователя"""
    user = User(
        email="user2@test.com",
        first_name="Test2",
        last_name="User2",
        phone="+1234567891",
        role=USER,
        is_active=True
    )
    user.password = make_password("testpass123")
    user.save()

    # Проверка корректности создания
    assert user.pk is not None
    assert user.email == "user2@test.com"
    return user


@pytest.fixture
def advertisement(regular_user):
    """Фикстура для создания тестового объявления"""
    ad = Advertisement.objects.create(
        title='Test Ad',
        price=1000,
        description='Test description',
        author=regular_user
    )
    assert ad.pk is not None
    return ad


@pytest.fixture
def review(regular_user, advertisement):
    """Фикстура для создания тестового отзыва"""
    rev = Review.objects.create(
        text='Great product!',
        author=regular_user,
        advertisement=advertisement
    )
    assert rev.pk is not None
    return rev