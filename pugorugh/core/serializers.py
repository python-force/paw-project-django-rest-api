from django.contrib.auth import get_user_model
from pugorugh.core.models import Profile

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        profile = Profile.objects.create(user=user)
        profile.bio = "About" + user.username
        profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    """
    A profile serializer to return the profile / user details
    """

    class Meta:
        model = Profile
        fields = ('age', 'gender', 'size')

    """
    def create(self, validated_data):
        
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of profile
        :return: returns a successfully created profile record
       
        user_data = validated_data['user']
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = Profile.objects.update_or_create(user=user,
                            bio=validated_data['bio'])
        return profile

    """
