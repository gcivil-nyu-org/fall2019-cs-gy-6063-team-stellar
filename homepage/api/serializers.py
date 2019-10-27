from rest_framework import serializers

from homepage.models import UserRequest

class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        field = ['school', 'department']
