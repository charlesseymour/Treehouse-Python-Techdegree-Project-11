from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django_webtest import WebTest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Dog, UserPref, UserDog


class ModelTests(WebTest):
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
    fixtures = ['all']

    def test_user_register(self):
        url = reverse('register-user')
        data = {'username': 'test_user_2', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=2).username, 'test_user_2')
        self.assertTrue(User.objects.get(id=2).check_password('password'))

    def test_retrieve_user_pref_with_token(self):
        url = reverse('userpref-detail')
        token = Token.objects.get(user__username='test_user')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(response.data['age'], ['b', 'y', 'a'])
        self.assertCountEqual(response.data['gender'], ['m', 'f'])
        self.assertCountEqual(response.data['size'], ['s', 'm', 'l'])

    def test_retrieve_user_pref_without_token(self):
        url = reverse('userpref-detail')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_pref_with_token(self):
        url = reverse('userpref-detail')
        user = User.objects.get()
        data = {'user': user.id, 'age': 'b', 'gender': 'm', 'size': 's,m,l'}
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(url, data, format='json')
        user_pref = UserPref.objects.get(user=user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_pref.age, ['b'])
        self.assertEqual(user_pref.gender, ['m'])
        self.assertCountEqual(user_pref.size, ['s', 'm', 'l'])

    def test_update_user_pref_without_token(self):
        url = reverse('userpref-detail')
        user = User.objects.get()
        data = {'user': user.id, 'age': 'b', 'gender': 'm', 'size': 's,m,l'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_first_undecided_dog(self):
        kwargs = {'pk': '-1', 'reaction': 'undecided'}
        url = reverse('next-detail', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 8)

    def test_get_second_undecided_dog(self):
        kwargs = {'pk': '8', 'reaction': 'undecided'}
        url = reverse('next-detail', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 9)

    def test_get_first_liked_dog(self):
        kwargs = {'pk': '-1', 'reaction': 'liked'}
        url = reverse('next-detail', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 2)

    def test_get_second_liked_dog(self):
        kwargs = {'pk': '2', 'reaction': 'liked'}
        url = reverse('next-detail', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 4)

    def test_get_first_disliked_dog(self):
        kwargs = {'pk': '-1', 'reaction': 'disliked'}
        url = reverse('next-detail', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 6)

    def test_get_second_disliked_dog(self):
        kwargs = {'pk': '6', 'reaction': 'disliked'}
        url = reverse('next-detail', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 7)

    def test_get_dog_without_token(self):
        kwargs = {'pk': '6', 'reaction': 'disliked'}
        url = reverse('next-detail', kwargs=kwargs)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_liked_dog_to_undecided(self):
        kwargs = {'pk': 2, 'reaction': 'undecided'}
        url = reverse('react-update', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserDog.objects.count(), 3)
        with self.assertRaises(UserDog.DoesNotExist):
            UserDog.objects.get(dog=2)

    def test_change_undecided_dog_to_disliked(self):
        kwargs = {'pk': 8, 'reaction': 'disliked'}
        url = reverse('react-update', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserDog.objects.count(), 5)
        self.assertEqual(UserDog.objects.filter(dog=8).count(), 1)

    def test_change_disliked_dog_to_liked(self):
        kwargs = {'pk': 6, 'reaction': 'liked'}
        url = reverse('react-update', kwargs=kwargs)
        user = User.objects.get()
        token = Token.objects.get(user__username=user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserDog.objects.count(), 4)
        self.assertEqual(UserDog.objects.get(dog=6).status, 'l')

    def test_change_status_without_token(self):
        kwargs = {'pk': 6, 'reaction': 'liked'}
        url = reverse('react-update', kwargs=kwargs)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
