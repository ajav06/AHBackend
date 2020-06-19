from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from .models import User, Player, Table


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        player = Player()
        player.name = user
        player.save()
        return user

class PlayerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.username')

    class Meta:
        model = Player
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = '__all__'

