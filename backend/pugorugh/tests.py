from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_webtest import WebTest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .models import Dog, UserPref, UserDog

class MenuTests(WebTest):
    def setUp(self):
        Dog.objects.create(
            name='Wanchan',
            image_filename='1.jpg',
            breed='Akita',
            age=30,
            gender='m',
            size='l'
        )
        User.objects.create_user('temporary', 'temp@example.com',
                                 'temporary')
        
    def test_dog_creation(self):
        dog = Dog.objects.get(name='Wanchan')
        self.assertEqual(dog.name, 'Wanchan')
        self.assertEqual(dog.image_filename, '1.jpg')
        self.assertEqual(dog.breed, 'Akita')
        self.assertEqual(dog.age, 30)
        self.assertEqual(dog.gender, 'm')
        self.assertEqual(dog.size, 'l')
        self.assertEqual(dog.age_stage, 'y')
        
    def test_user_pref_creation(self):
        user = User.objects.get(username='temporary')
        user_pref = UserPref.objects.create(age='b,y',
                                            gender='m,f',
                                            size='s,m',
                                            user=user)
        self.assertEqual(user_pref.user, user)
        self.assertEqual(user_pref.age, 'b,y')
        self.assertEqual(user_pref.gender, 'm,f')
        self.assertEqual(user_pref.size, 's,m')
        
    def test_user_dog_creation(self):
        user = User.objects.get(username='temporary')
        dog = Dog.objects.get(name='Wanchan')
        user_dog = UserDog.objects.create(user=user,
                                          dog=dog,
                                          status='l')
        self.assertEqual(user_dog.user, user)
        self.assertEqual(user_dog.dog, dog)
        self.assertEqual(user_dog.status, 'l')
        
class ViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temp@example.com',
                                 'temporary')
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()
        self.user_pref = UserPref.objects.create(age='b,y',
                                            gender='m,f',
                                            size='s,m',
                                            user=self.user)
        self.user_pref.save()
        
    def test_user_register(self):
        url = reverse('register-user')
        data = {'username': 'test_user', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, 'test_user')
        self.assertTrue(User.objects.get(id=2).check_password('password'))
        
    def test_retrieve_user_pref_with_token(self):
        url = reverse('userpref-detail')
        token = Token.objects.get(user__username='temporary')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['age']), 2)
        self.assertIn('b', response.data['age'])
        self.assertIn('y', response.data['age'])
        self.assertEqual(len(response.data['gender']), 2)
        self.assertIn('m', response.data['gender'])
        self.assertIn('f', response.data['gender'])
        self.assertEqual(len(response.data['size']), 2)
        self.assertIn('s', response.data['size'])
        self.assertIn('m', response.data['size'])
        
    def test_retrieve_user_pref_without_token(self):
        url = reverse('userpref-detail')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_user_pref_with_token(self):
        url = reverse('userpref-detail')
        data = {'user': self.user.id, 'age': 'b', 'gender': 'm', 'size': 's,m,l'}
        token = Token.objects.get(user__username='temporary')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(url, data, format='json')
        print(response)
        
        
        
        
        
        
        
        
        
        
        

