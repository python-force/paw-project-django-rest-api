from django.contrib.auth import get_user_model

from rest_framework import permissions
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


class UserProfileView(APIView):
    """
    A class based view for creating and fetching student records
    """
    def get(self, format=None):
        """
        Get the user profile
        :param format: Format of the user profile
        :return: Returns a list user preferences
        """
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

