from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from rest_framework.serializers import (ModelSerializer,ValidationError,EmailField,)
from rest_framework import serializers
import rest_framework.serializers as serializers
from rest_framework.serializers import (
ModelSerializer,
ValidationError,
EmailField,
)


from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data): 
        user = authenticate(**data)

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            data['tokens'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return data

        raise serializers.ValidationError("Incorrect Credentials")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'tokens' in data:
            tokens = data.pop('tokens')
            data.update(tokens)
        return data