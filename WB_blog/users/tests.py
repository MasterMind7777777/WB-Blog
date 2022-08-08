from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class TestUserAuth(APITestCase):

    def test_sign_up(self):
        data = {'username': 'test_user', 'password': 'Qdwq1234'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_log_in(self):
        data = {'username': 'test_user', 'password': 'Qdwq1234'}
        self.client.post('/api/users/', data)
        response = self.client.post('/api/auth/token/login/', data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# class TestUserMange(APITestCase):

#     def setUp(self):
#         client = APIClient()
#         client.login(username='lauren', password='secret')
#         token = Token.objects.get(user__username='lauren')
#         client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

#     def test_log_out(self):
#         response = self.client.post('/api/auth/token/logout/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
