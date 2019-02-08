import random
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView

from pugorugh.core.serializers import UserSerializer, ProfileSerializer, DogSerializer
from pugorugh.core.models import Profile, Dog


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


class UpdateUserDogView(RetrieveUpdateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer