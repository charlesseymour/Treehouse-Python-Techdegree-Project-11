from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_webtest import WebTest
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

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
    def test_user_register(self):
        url = reverse('register-user')
        data = {'username': 'temporary', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'temporary')
        self.assertTrue(User.objects.get().check_password('password'))
        
        
        
        

