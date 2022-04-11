from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.models import UserManager

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "first_name", "last_name"]


class UserManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManager
        fields = '__al__'
