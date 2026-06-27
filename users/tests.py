from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class UserRegistrationTest(TestCase):

    def test_user_registration(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'Иван',
                'password1': 'TestPassword123!',
                'password2': 'TestPassword123!'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            User.objects.filter(
                username='Иван'
            ).exists()
        )

class UserProfileTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'Пользователь',
            password = 'TestPassword123!'
        )

    def test_profile_requires_login(self):
        response = self.client.get(
            reverse('profile')
        )

        self.assertEqual(response.status_code, 302)

    def test_profile_page_for_authorized_user(self):
        self.client.login(
            username = 'Пользователь',
            password = 'TestPassword123!'
        )

        response = self.client.get(
            reverse('profile')
        )

        self.assertEqual(response.status_code, 200)

    def test_profile_contains_statistics(self):
        self.client.login(
            username = 'Пользователь',
            password = 'TestPassword123!'
        )

        response = self.client.get(
            reverse('profile')
        )

        self.assertContains(
            response,
            '0'
        )