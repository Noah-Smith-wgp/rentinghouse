from rest_framework import serializers

from apps.users.models import User


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
