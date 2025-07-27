import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import make_password
from advertisements.models import Advertisement, Review
from users.models import User, USER, ADMIN

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
        is_active=True
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
        is_active=True
    )
    user.password = make_password("adminpass123")
    user.save()
    return user

@pytest.fixture
def second_user():
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
    return user

@pytest.fixture
def advertisement(regular_user):
    return Advertisement.objects.create(
        title='Test Ad',
        price=1000,
        description='Test description',
        author=regular_user
    )

@pytest.fixture
def review(regular_user, advertisement):
    return Review.objects.create(
        text='Great product!',
        author=regular_user,
        advertisement=advertisement
    )

# Тесты моделей
class TestModels:
    def test_advertisement_creation(self, advertisement, regular_user):
        assert advertisement.title == 'Test Ad'
        assert advertisement.price == 1000
        assert advertisement.author == regular_user
        assert advertisement.created_at is not None

    def test_review_creation(self, review, regular_user, advertisement):
        assert review.text == 'Great product!'
        assert review.author == regular_user
        assert review.advertisement == advertisement
        assert review.created_at is not None

# Тесты API объявлений
class TestAdvertisementAPI:
    def test_anonymous_can_view_ads(self, api_client, advertisement):
        url = reverse('advertisement-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_user_can_create_ad(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        url = reverse('advertisement-list')
        data = {
            'title': 'New Ad',
            'price': 2000,
            'description': 'Test'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['author']['email'] == 'user@test.com'

    def test_user_can_edit_own_ad(self, api_client, regular_user, advertisement):
        api_client.force_authenticate(user=regular_user)
        url = reverse('advertisement-detail', args=[advertisement.id])
        data = {'title': 'Updated Title'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'

    def test_user_cant_edit_other_user_ad(self, api_client, second_user, advertisement):
        api_client.force_authenticate(user=second_user)
        url = reverse('advertisement-detail', args=[advertisement.id])
        data = {'title': 'Updated Title'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_edit_any_ad(self, api_client, admin_user, advertisement):
        api_client.force_authenticate(user=admin_user)
        url = reverse('advertisement-detail', args=[advertisement.id])
        data = {'title': 'Admin Updated'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

# Тесты API отзывов
class TestReviewAPI:
    def test_anonymous_can_view_reviews(self, api_client, advertisement, review):
        url = reverse('review-list', args=[advertisement.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_user_can_create_review(self, api_client, second_user, advertisement):
        api_client.force_authenticate(user=second_user)
        url = reverse('review-list', args=[advertisement.id])
        data = {'text': 'New review'}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['author']['email'] == 'user2@test.com'

    def test_user_can_edit_own_review(self, api_client, regular_user, advertisement, review):
        api_client.force_authenticate(user=regular_user)
        url = reverse('review-detail', args=[advertisement.id, review.id])
        data = {'text': 'Updated review'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_cant_edit_other_user_review(self, api_client, second_user, advertisement, review):
        api_client.force_authenticate(user=second_user)
        url = reverse('review-detail', args=[advertisement.id, review.id])
        data = {'text': 'Updated review'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

# Тесты фильтрации и пагинации
class TestAdvertisementFilters:
    @pytest.fixture(autouse=True)
    def setup(self, regular_user):
        Advertisement.objects.create(
            title='Laptop',
            price=1000,
            author=regular_user
        )
        Advertisement.objects.create(
            title='Phone',
            price=500,
            author=regular_user
        )

    def test_filter_by_title(self, api_client):
        url = reverse('advertisement-list') + '?title=top'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Laptop'

class TestAdvertisementPagination:
    @pytest.fixture(autouse=True)
    def setup(self, regular_user):
        for i in range(5):
            Advertisement.objects.create(
                title=f'Ad {i}',
                price=100 + i,
                author=regular_user
            )

    def test_pagination(self, api_client):
        url = reverse('advertisement-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 4
        assert response.data['next'] is not None