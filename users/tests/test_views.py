from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

User = get_user_model()


class CreateUserViewTests(APITestCase):
    def test_create_user(self):
        """
        Test creating a new user.
        """
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post("/api/users/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

    def test_create_user_with_existing_email(self):
        """
        Test creating a user with an existing email.
        """
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="existingpassword",
        )
        data = {
            "username": "testuser",
            "email": "existing@example.com",
            "password": "testpassword123",
        }
        response = self.client.post("/api/users/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_invalid_data(self):
        """
        Test creating a user with invalid data.
        """
        data = {
            "username": "",
            "email": "invalidemail",
            "password": "pass",
        }
        response = self.client.post("/api/users/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class CreateAuthTokenViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )

    def test_create_auth_token(self):
        """
        Test creating a new authentication token.
        """
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post("/api/users/auth-token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        token_key = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token_key).exists())

    def test_create_auth_token_invalid_credentials(self):
        """
        Test creating an authentication token with invalid credentials
        """
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post("/api/users/auth-token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_create_auth_token_missing_fields(self):
        """
        Test creating an authentication token with missing fields.
        """
        data = {
            "email": "test@example.com",
        }
        response = self.client.post("/api/users/auth-token/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpassword"
        )
        self.token = Token.objects.create(user=self.user)

    def test_logout_successful(self):
        """
        Test successful logout.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token.key)
        response = self.client.delete("/api/users/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
        self.assertEqual(response.data["detail"], "Logout successful")

    def test_logout_without_authentication(self):
        """
        Test logout without authentication .
        """
        response = self.client.delete("/api/users/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(key=self.token.key).exists())

    def test_logout_with_invalid_token(self):
        """
        Test logout with invalid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = self.client.delete("/api/users/logout/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Token.objects.filter(key=self.token.key).exists())
