from rest_framework import serializers
from .models import User

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','is_verified','is_staff']


class VerifySerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20)
    class Meta:
        model = User
        fields = ['password']