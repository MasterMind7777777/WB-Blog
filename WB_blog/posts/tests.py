from django.test import TestCase


    # def test_read_post(self):
    #     response = self.client2.post('/api/users/1/read/')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'not loged in')

    #     response = self.client2.post('/api/auth/token/login/', self.data)
    #     token2 = response.json()['auth_token']
    #     self.client2.credentials(HTTP_AUTHORIZATION='Token ' + token2)

    #     response = self.client.get('/api/posts/')
    #     print(str(response.json()))
    #     post_id = str(response.json()['results'][0])

    #     response = self.client2.post('/api/users/' + post_id +'/read/')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'loged in')

    #     response = self.client2.post('/api/users/' + post_id +'/read/')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'loged in alredy marked as read')