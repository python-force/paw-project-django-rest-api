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
    permission_classes = (permissions.AllowAny,)

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
            location='Brooklyn',
            age='a,s',
            gender='m,f',
            size='s,m,l,xl'
        )

    def test_update_profile(self):
        """
        Ensure we can create a new account object.
        """
        self.client.login(username='johnconnor', password='terminator')
        url = reverse('user-preferences')
        data = {"bio": "Aboutdude",
                "location": "",
                "age": "a,s",
                "gender": "m,f",
                "size": "s,m,l,xl"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.profile, 1)
        # self.assertEqual(self.profile.bio, 'Aboutdude')


class NextDogViewTests(APITestCase):
    """Testing NextDogAPI View"""
    def setUp(self):
        """Creating User"""
        self.user = User.objects.create_user(
            username='johnconnor',
            email='dude@nasa.gov',
            password='terminator'
        )
        self.person = Profile.objects.create(
            user=self.user,
            bio='About',
            location='Brooklyn',
            age='a,s',
            gender='m,f',
            size='s,m,l,xl'
        )

        """Creating 3 Dogs"""
        self.dog = Dog.objects.create(
            name='Francesca',
            image_filename='1.jpg',
            breed='Labrador',
            age=72,
            gender='l',
            size='f'
        )
        self.dog2 = Dog.objects.create(
            name='Hank',
            image_filename='2.jpg',
            breed='French Bulldog',
            age=14,
            gender='xl',
            size='f'
        )
        self.dog3 = Dog.objects.create(
            name='Muffin',
            image_filename='3.jpg',
            breed='French Bulldog',
            age=36,
            gender='m',
            size='m'
        )

    def test_detect_user(self):
        user_obj = Profile.objects.get(user=self.user)
        self.assertEqual(user_obj.user.username, 'johnconnor')

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        dog1 = Dog.objects.get(name="Francesca")
        dog2 = Dog.objects.get(name="Hank")
        self.assertEqual(dog1.breed, 'Labrador')
        self.assertEqual(dog2.breed, 'French Bulldog')


"""
    def test_index(self):
        #Testing Mineral List View
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')

    def test_mineral_detail_view(self):
        #Testing Mineral Detail View
        resp = self.client.get(reverse('detail',
                                       kwargs={'pk': self.mineral.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mineral, resp.context['mineral'])
        self.assertTemplateUsed(resp, 'detail.html')

    def test_search_q(self):
        #Testing Search View by Alphabet
        resp = self.client.get(reverse('search'), {'q': 'G'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')

    def test_search_q2(self):
        #Testing Search View by Alphabet 404
        resp = self.client.get(reverse('search'), {'q': 'X'})
        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed(resp, '404.html')

    def test_search_group(self):
        #Testing Search View by Group
        resp = self.client.get(reverse('search'), {'group': 'Sulfides'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')

    def test_search_text(self):
        #Testing Search View by Full-Text Search
        resp = self.client.get(reverse('search'), {'text': 'Cubic'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context['minerals'])
        self.assertIn(self.mineral2, resp.context['minerals'])
        self.assertTemplateUsed(resp, 'index.html')
"""
