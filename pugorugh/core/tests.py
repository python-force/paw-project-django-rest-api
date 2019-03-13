from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework import permissions
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient
from rest_framework import status
from rest_framework.test import APITestCase
from pugorugh.core.models import Dog, UserDog, Profile

class UserRegisterViewTests(APITestCase):
    """Testing Create User"""

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register-user')
        data = {'username':'johnconnor', 'email':'dude@nasa.gov', 'password':'terminator'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'johnconnor')


class RetrieveUpdateProfileViewTests(APITestCase):

    """Updating Profile"""
    def setUp(self):
        """Creating User"""
        self.user = User.objects.create_user(
            username='johnconnor',
            email='dude@nasa.gov',
            password='terminator'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='About',
            location='Florida',
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )
        self.client.login(username='johnconnor', password='terminator')
        

    def test_update_profile(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user-preferences')
        data = {"bio": "About John",
                "location": "Brooklyn",
                "age": "b,y,a,s",
                "gender": "m,f",
                "size": "s,m,l,xl"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user.username, 'johnconnor')
        self.assertEqual(self.profile.bio, 'About John')
        self.assertEqual(self.profile.location, 'Brooklyn')


class NextDogViewTests(APITestCase):
    """Testing NextDogAPI View"""
    def setUp(self):
        """Creating User"""
        self.user = User.objects.create_user(
            username='johnconnor',
            email='dude@nasa.gov',
            password='terminator'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='About',
            location='Brooklyn',
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )

        """Creating 4 Dogs"""
        self.dog = Dog.objects.create(
            name='Sky',
            image_filename='3.jpg',
            breed='Daschund',
            age=18,
            gender='m',
            size='s'
        )
        self.dog2 = Dog.objects.create(
            name='Muffin',
            image_filename='4.jpg',
            breed='Labrador',
            age=29,
            gender='m',
            size='xl'
        )
        self.dog3 = Dog.objects.create(
            name='Zeus',
            image_filename='1.jpg',
            breed='Jack Russell',
            age=60,
            gender='m',
            size='m'
        )
        self.dog4 = Dog.objects.create(
            name='Athena',
            image_filename='2.jpg',
            breed='Jack Russell',
            age=192,
            gender='f',
            size='l'
        )
        self.client.login(username='johnconnor', password='terminator')

    def test_animals_exists(self):
        """Animals Exists"""
        dog1 = Dog.objects.get(name="Sky")
        dog2 = Dog.objects.get(name="Muffin")
        dog3 = Dog.objects.get(name="Zeus")
        dog4 = Dog.objects.get(name="Athena")
        self.assertEqual(dog1.id, 1)
        self.assertEqual(dog2.id, 2)
        self.assertEqual(dog3.id, 3)
        self.assertEqual(dog4.id, 4)

    def test_next_dog_view_pass(self):
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_next_dog_view_baby(self):
        self.profile.age = 'b'
        self.profile.save()
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1,
                                         'name': 'Sky',
                                         'image_filename': '3.jpg',
                                         'breed': 'Daschund',
                                         'age': 18,
                                         'gender': 'm',
                                         'size': 's'})

    def test_next_dog_view_young(self):
        self.profile.age = 'y'
        self.profile.save()
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 2,
                                         'name': 'Muffin',
                                         'image_filename': '4.jpg',
                                         'breed': 'Labrador',
                                         'age': 29,
                                         'gender': 'm',
                                         'size': 'xl'})

    def test_next_dog_view_adult(self):
        self.profile.age = 'a'
        self.profile.save()
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 3,
                                         'name': 'Zeus',
                                         'image_filename': '1.jpg',
                                         'breed': 'Jack Russell',
                                         'age': 60,
                                         'gender': 'm',
                                         'size': 'm'})

    def test_next_dog_view_senior(self):
        self.profile.age = 's'
        self.profile.save()
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 4,
                                         'name': 'Athena',
                                         'image_filename': '2.jpg',
                                         'breed': 'Jack Russell',
                                         'age': 192,
                                         'gender': 'f',
                                         'size': 'l'})

    def test_next_dog_view_gender_only_one(self):
        self.profile.gender = 'f'
        self.profile.save()
        url = reverse('dog-filter-detail', kwargs={'pk': self.dog.id, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 4,
                                         'name': 'Athena',
                                         'image_filename': '2.jpg',
                                         'breed': 'Jack Russell',
                                         'age': 192,
                                         'gender': 'f',
                                         'size': 'l'})

    def test_next_dog_view_gender_404_not_found(self): # raise Http404 - test is working but not removing in HTML
        self.profile.gender = ''
        self.profile.save()
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'undecided'})
        data = {}
        response = self.client.get(url, data, format='json')
        # print(response.status_code)
        # print(dir(status))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateUserDogViewTests(APITestCase):
    """Testing NextDogAPI View"""

    def setUp(self):
        """Creating User"""
        self.user = User.objects.create_user(
            username='johnconnor',
            email='dude@nasa.gov',
            password='terminator'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio='About',
            location='Brooklyn',
            age='b,y,a,s',
            gender='m,f',
            size='s,m,l,xl'
        )

        """Creating 4 Dogs"""
        self.dog = Dog.objects.create(
            name='Sky',
            image_filename='3.jpg',
            breed='Daschund',
            age=18,
            gender='m',
            size='s'
        )
        self.dog2 = Dog.objects.create(
            name='Muffin',
            image_filename='4.jpg',
            breed='Labrador',
            age=29,
            gender='m',
            size='xl'
        )
        self.dog3 = Dog.objects.create(
            name='Zeus',
            image_filename='1.jpg',
            breed='Jack Russell',
            age=60,
            gender='m',
            size='m'
        )
        self.dog4 = Dog.objects.create(
            name='Athena',
            image_filename='2.jpg',
            breed='Jack Russell',
            age=192,
            gender='f',
            size='l'
        )
        self.client.login(username='johnconnor', password='terminator')

        # Having 1st dog liked in UserDog
        url = reverse('dog-list', kwargs={'pk': 1, 'status': 'liked'})
        data = {}
        self.client.put(url, data, format='json')

        # Having 2nd dog disliked in UserDog
        url = reverse('dog-list', kwargs={'pk': 4, 'status': 'disliked'})
        data = {}
        self.client.put(url, data, format='json')

    # Test to make sure the Dog is being liked in UserDog Table
    def test_update_userdog_view_dog_exists_liked(self):
        dog = Dog.objects.filter(dogtag__status='liked').filter(dogtag__user_id=self.user.id).first()
        self.assertEqual(dog.name, 'Sky')
        self.assertEqual(Dog.objects.filter(dogtag__status='liked').filter(dogtag__user_id=self.user.id).exists(), True)

    def test_animals_exists(self):
        """Animals Exists"""
        dog1 = Dog.objects.get(name="Sky")
        dog2 = Dog.objects.get(name="Muffin")
        dog3 = Dog.objects.get(name="Zeus")
        dog4 = Dog.objects.get(name="Athena")
        self.assertEqual(dog1.id, 1)
        self.assertEqual(dog2.id, 2)
        self.assertEqual(dog3.id, 3)
        self.assertEqual(dog4.id, 4)

    def test_update_userdog_view_pass(self):
        url = reverse('dog-list', kwargs={'pk': 1, 'status': 'liked'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_userdog_view_perform_update(self):
        url = reverse('dog-list', kwargs={'pk': 1, 'status': 'liked'})
        data = {'id': 1,
                'name': 'Sky',
                'image_filename': '3.jpg',
                'breed': 'Daschund',
                'age': 15,
                'gender': 'm',
                'size': 's'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.dog.refresh_from_db()
        self.assertEqual(self.dog.age, 15)

    def test_next_dog_view_userdog_query_liked(self):
        url = reverse('dog-filter-detail', kwargs={'pk': -1, 'dog_filter': 'liked'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dog = Dog.objects.filter(dogtag__status='liked').filter(dogtag__user_id=self.user.id).first()
        self.assertEqual(dog.name, 'Sky')

    def test_next_dog_view_userdog_query_not_exist_liked(self):
        url = reverse('dog-filter-detail', kwargs={'pk': 1, 'dog_filter': 'liked'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_next_dog_view_userdog_query_disliked(self):
        url = reverse('dog-filter-detail', kwargs={'pk': 3, 'dog_filter': 'disliked'})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dog = Dog.objects.filter(dogtag__status='disliked').filter(dogtag__user_id=self.user.id).first()
        self.assertEqual(dog.name, 'Athena')

    def test_update_userdog_view_disliked(self):
        url = reverse('dog-list', kwargs={'pk': 1, 'status': 'undecided'})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Dog.objects.filter(dogtag__status='liked').filter(dogtag__user_id=self.user.id).exists())

    def test_update_userdog_view_changing_liked_to_disliked(self):
        url = reverse('dog-list', kwargs={'pk': 1, 'status': 'disliked'})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dog = Dog.objects.filter(dogtag__status='disliked').filter(dogtag__user_id=self.user.id).first()
        self.assertEqual(dog.name, 'Sky')
        self.assertTrue(Dog.objects.filter(dogtag__status='disliked').filter(dogtag__user_id=self.user.id).exists())

    def test_update_userdog_view_adding_dislike_to_already_liked_dogs(self):
        url = reverse('dog-list', kwargs={'pk': 2, 'status': 'disliked'})
        data = {}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dog = Dog.objects.filter(dogtag__status='disliked').filter(dogtag__user_id=self.user.id).first()
        self.assertEqual(dog.name, 'Muffin')
        self.assertTrue(Dog.objects.filter(dogtag__status='disliked').filter(dogtag__user_id=self.user.id).exists())

    def test_update_userdog_view_bad_status(self):
        data = {'pk': 1, 'status': 'notanoption'}
        url = reverse('dog-list', kwargs=data)
        # attempt to PUT request the bad status data to that route.
        response = self.client.put(url, data, format='json')

        # Does not exist because of wrong status
        self.assertEqual(response.status_code, 404)


    """
    def test_update_userdog_view_adding_dislike_to_already_liked_dogs(self):
        data = {'pk': 1, 'status': 'liked'}
        url = reverse('dog-list', kwargs=data)
        # attempt to PUT request the data to that route.
        response = self.client.put(url, data, format='json')

        pk = response.data.get('id', 0)  # default to 0 if no 'id' key.

        # if the PUT performs correctly, the API should return JSON
        # with the same dog PK.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(pk, data.get('pk'))
        
    """




