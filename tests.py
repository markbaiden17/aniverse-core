"""
AniVerse Core — Unit Tests
Comprehensive test suite covering Authentication, Reviews, Watchlist, and Analytics.
Run with: python manage.py test
"""

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.reviews.models import Review
from apps.watchlist.models import WatchlistEntry

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def create_user(username='testuser', password='TestPass123'):
    """Utility to create a user and return an associated Auth Token."""
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token

# -----------------------------------------------------------------------------
# Authentication Tests
# -----------------------------------------------------------------------------

class RegisterTests(APITestCase):
    """Test user registration flow and validation logic."""
    url = '/api/auth/register/'

    def test_register_success(self):
        data = {'username': 'newuser', 'email': 'new@test.com', 'password': 'SecurePass1'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_username(self):
        User.objects.create_user(username='dupeuser', password='pass1234')
        data = {'username': 'dupeuser', 'email': 'other@test.com', 'password': 'pass1234'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        data = {'username': 'shortpass', 'email': 'x@test.com', 'password': '123'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    """Test user authentication and token retrieval."""
    url = '/api/auth/login/'

    def setUp(self):
        self.user, _ = create_user()

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'TestPass123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'WrongPass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        response = self.client.post(self.url, {'username': 'ghost', 'password': 'anything'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------
# Review System Tests
# -----------------------------------------------------------------------------

class ReviewListCreateTests(APITestCase):
    """Test review creation, duplicate prevention, and public listing."""
    url = '/api/reviews/'

    def setUp(self):
        self.user, self.token = create_user()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_review_success(self):
        # Checks for correct data storage and username injection in response
        data = {'media_id': 1, 'rating': 9, 'comment': 'Great anime!'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 9)
        self.assertEqual(response.data['username'], self.user.username)

    def test_create_review_unauthenticated(self):
        self.client.credentials()
        data = {'media_id': 2, 'rating': 7, 'comment': 'Nice'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review_rating_too_high(self):
        # Range validation test (max 10)
        data = {'media_id': 3, 'rating': 11, 'comment': 'Out of range'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_rating_too_low(self):
        # Range validation test (min 1)
        data = {'media_id': 4, 'rating': 0, 'comment': 'Zero rating'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_review_rejected(self):
        # Enforces one review per user per anime
        data = {'media_id': 5, 'rating': 8, 'comment': 'First review'}
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_reviews_public(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_media_id(self):
        # Verifies custom filter backend for media_id lookups
        Review.objects.create(user=self.user, media_id=100, rating=7, comment='A')
        Review.objects.create(user=self.user, media_id=200, rating=8, comment='B')
        response = self.client.get(self.url + '?media_id=100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['media_id'], 100)


class ReviewDetailTests(APITestCase):
    """Test Object-Level Permissions: Only owners can modify their reviews."""

    def setUp(self):
        self.owner, self.owner_token = create_user('owner', 'OwnerPass1')
        self.other, self.other_token = create_user('other', 'OtherPass1')
        self.review = Review.objects.create(
            user=self.owner, media_id=10, rating=8, comment='Original comment'
        )
        self.url = f'/api/reviews/{self.review.id}/'

    def test_retrieve_review_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['comment'], 'Original comment')

    def test_update_own_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.owner_token.key}')
        response = self.client.patch(self.url, {'rating': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rating'], 10)

    def test_update_other_users_review_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.other_token.key}')
        response = self.client.patch(self.url, {'rating': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_review(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.owner_token.key}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_users_review_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.other_token.key}')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_nonexistent_review(self):
        response = self.client.get('/api/reviews/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# -----------------------------------------------------------------------------
# Watchlist Tests
# -----------------------------------------------------------------------------

class WatchlistTests(APITestCase):
    """Test private watchlist management and status updates."""
    url = '/api/watchlist/'

    def setUp(self):
        self.user, self.token = create_user('watcher', 'WatchPass1')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_add_to_watchlist(self):
        data = {'media_id': 50, 'status': 'watching'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'watching')

    def test_watchlist_requires_auth(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_watchlist_only_shows_own_entries(self):
        # Privacy check: Ensure data isolation between users
        WatchlistEntry.objects.create(user=self.user, media_id=60, status='completed')
        other, _ = create_user('other_watcher', 'OtherPass2')
        WatchlistEntry.objects.create(user=other, media_id=70, status='watching')

        response = self.client.get(self.url)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['media_id'], 60)

    def test_duplicate_watchlist_entry_rejected(self):
        data = {'media_id': 80, 'status': 'plan_to_watch'}
        self.client.post(self.url, data)
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_watchlist_status(self):
        entry = WatchlistEntry.objects.create(user=self.user, media_id=90, status='plan_to_watch')
        response = self.client.patch(f'{self.url}{entry.id}/', {'status': 'completed'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_delete_watchlist_entry(self):
        entry = WatchlistEntry.objects.create(user=self.user, media_id=95, status='watching')
        response = self.client.delete(f'{self.url}{entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------------------
# Statistical Data Tests
# -----------------------------------------------------------------------------

class StatsTests(APITestCase):
    """Test rating aggregation math and distribution logic."""

    def setUp(self):
        u1, _ = create_user('stat_user1', 'Pass1234!')
        u2, _ = create_user('stat_user2', 'Pass5678!')
        u3, _ = create_user('stat_user3', 'Pass9999!')
        Review.objects.create(user=u1, media_id=999, rating=8, comment='')
        Review.objects.create(user=u2, media_id=999, rating=10, comment='')
        Review.objects.create(user=u3, media_id=999, rating=6, comment='')

    def test_stats_returns_correct_average(self):
        response = self.client.get('/api/stats/999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_reviews'], 3)
        self.assertEqual(float(response.data['average_rating']), 8.0)

    def test_stats_no_reviews(self):
        # Edge case: Anime with zero reviews
        response = self.client.get('/api/stats/00000/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_reviews'], 0)
        self.assertIsNone(response.data['average_rating'])

    def test_stats_is_public(self):
        response = self.client.get('/api/stats/999/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stats_rating_distribution(self):
        # Verifies correct tally for each rating score (1-10)
        response = self.client.get('/api/stats/999/')
        dist = response.data['rating_distribution']
        self.assertEqual(dist['8'], 1)
        self.assertEqual(dist['10'], 1)
        self.assertEqual(dist['6'], 1)
        self.assertEqual(dist['1'], 0)