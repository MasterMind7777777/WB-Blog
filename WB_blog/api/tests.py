from rest_framework.test import APIClient
from rest_framework.test import APITestCase

class TestBase(APITestCase):

    def setUp(self):
        self.data = {'username': 'test_user', 'password': 'Qdwq1234'}
        self.data2 = {'username': 'test_user2', 'password': 'Qdwq1234'}
        self.post = {"name": "test post name", "text": "test post text"}
        self.post2 = {"name": "test post name2", "text": "test post text2"}
        self.client.post('/api/users/', self.data)
        self.client2 = APIClient()
        self.client2.post('/api/users/', self.data2)
        response = self.client.post('/api/auth/token/login/', self.data)
        self.token = response.json()['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.client.post('/api/posts/', self.post)
        self.client.post('/api/posts/', self.post2)