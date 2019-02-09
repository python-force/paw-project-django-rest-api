import random
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from pugorugh.core.serializers import UserSerializer, ProfileSerializer, DogSerializer
from pugorugh.core.models import Profile, Dog, UserDog

from pugorugh.core.serializers import DogSerializer


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class ListProfileView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RetrieveUpdateProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.get_queryset()
        user_pref = get_object_or_404(queryset, user=self.request.user)
        return user_pref

    """
    def put(self, request, *args, **kwargs):
        import pdb;
        pdb.set_trace()
        response = super().put(*args, **kwargs)
        return response
    """

class RetrieveDogView(RetrieveAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_object(self):
        queryset = self.get_queryset()
        dog = queryset.first()
        return dog

class NextDogView(RetrieveUpdateAPIView):
    """Not Finished"""
    serializer_class = DogSerializer

    def get_queryset(self):
        qs = Dog.objects.filter(doguser__user=self.request.user)
        return qs

    def get_object(self):
        queryset = self.get_queryset()
        dog = queryset.first()
        return dog

    """
    def put(self, request, *args, **kwargs):
        user = self.request.user
        status = self.kwargs.get('status')
        dog = self.get_object()
        try:
            qs = self.get_queryset().get(dog=dog)
            qs.status = status
            qs.save()
        except:
            UserDog.objects.create(
                user=user,
                dog=dog,
                status=status
            )

        return super().put(request, *args, **kwargs)
    """

class UpdateUserDogView(RetrieveUpdateAPIView):
    serializer_class = DogSerializer

    def get_queryset(self):
        return UserDog.objects.filter(user=self.request.user)

    def get_object(self):
        dog = Dog.objects.get(id=7)
        return dog

    def put(self, request, *args, **kwargs):
        user = self.request.user
        status = self.kwargs.get('status')
        dog = Dog.objects.get(id=self.kwargs.get('pk'))

        if not self.get_queryset():
            UserDog.objects.create(
                user=user,
                dog=dog,
                status=status
            )
        else:
            try:
                qs = self.get_queryset().get(dog=dog)
                qs.status = status
                qs.save()
            except:
                UserDog.objects.create(
                    user=user,
                    dog=dog,
                    status=status
                )
        return super().put(request, *args, **kwargs)

    """
    def get_object(self):
        pk = self.kwargs.get('pk')
       
        if pk == 'undefined':
            dog = Dog.objects.first()
        else:
            dog = Dog.objects.get(id=self.kwargs.get('pk'))
       
        print(Dog.objects.get(id=3))
        return Dog.objects.get(id=3)
    """

    """
    def get_object(self):
        if self.kwargs.get('pk') != "-1":
            try:
                dog = self.queryset.get(id=self.kwargs.get('pk'))
                return dog
            except ObjectDoesNotExist:
                return None
        else:
            print('No Dog')
    """
