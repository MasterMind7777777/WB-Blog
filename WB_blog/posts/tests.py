from rest_framework import status
from api.tests import TestBase

class TestPosts(TestBase):
    
    def test_post_list(self):
        response = self.client2.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'not loged in')

        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'loged in')
    
    def test_post_detail(self):
        response = self.client2.get('/api/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get('/api/posts/')
        id1 = str(response.json()['results'][0]['id'])
        response = self.client.get('/api/posts/' + id1 + '/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_read(self):
        response = self.client2.post('/api/posts/1/read/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'not loged in')

        response = self.client2.post('/api/auth/token/login/', self.data)
        token2 = response.json()['auth_token']
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + token2)

        response = self.client.get('/api/posts/')
        id1 = str(response.json()['results'][0]['id'])

        response = self.client2.post('/api/posts/' + id1 +'/read/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'loged in')

        response = self.client2.post('/api/posts/' + id1 +'/read/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'loged in alredy read')
    
    def test_post_create(self):
        post_loc = {'name': 'name post loc', 'text': 'test text for post loc'}
        response = self.client2.post('/api/posts/', post_loc)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post('/api/posts/', post_loc)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
