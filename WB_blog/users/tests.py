from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.tests import TestBase

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestUserMange(TestBase):

    def test_log_out(self):
        response = self.client.post('/api/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post('/api/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_users_list(self):
        response = self.client2.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscribe(self):
        response = self.client2.post('/api/users/1/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'not loged in')

        response = self.client2.post('/api/auth/token/login/', self.data)
        token2 = response.json()['auth_token']
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + token2)

        response = self.client.get('/api/users/')
        id1 = str(response.json()['results'][0]['id'])
        id2 = str(response.json()['results'][1]['id'])

        response = self.client2.post('/api/users/' + id1 +'/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'loged in')

        response = self.client2.post('/api/users/' + id1 +'/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'loged in alredy sub')

        response = self.client2.post('/api/users/' + id2 +'/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'loged in self sub')

    def test_user_post(self):
        response = self.client2.get('/api/users/1/posts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get('/api/users/')
        id1 = str(response.json()['results'][0]['id'])
        response = self.client.post('/api/users/' + id1 + '/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_subscriptions_posts(self):
        response = self.client2.get('/api/users/subscriptions_posts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get('/api/users/subscriptions_posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)