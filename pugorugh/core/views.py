from django.contrib.auth import get_user_model

from rest_framework import permissions, generics
from rest_framework.generics import CreateAPIView

from pugorugh.core.serializers import UserSerializer, ProfileSerializer
from pugorugh.core.models import Profile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class ListProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer