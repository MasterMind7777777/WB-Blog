from rest_framework.test import APITestCase
from rest_framework import status

class TestUserAuth(APITestCase):

    def test_sign_up(self):
        data = {'username': 'test_user', 'password': 'Qdwq1234'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_log_in(self):
        data = {'username': 'test_user', 'password': 'Qdwq1234'}
        self.client.post('/api/users/', data)
        response = self.client.post('/api/auth/token/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    