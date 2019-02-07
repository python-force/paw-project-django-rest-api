from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView

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
        print(queryset)
        user_pref = get_object_or_404(queryset, user=self.request.user)
        print(self.request.user)
        print(user_pref)
        return user_pref


class ListDogView(ListAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer