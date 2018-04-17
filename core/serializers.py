from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Game


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    finished = serializers.SerializerMethodField()
    matrix = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id', 'user', 'width', 'height', 'mines', 'start_date', 'end_date',
                  'won', 'finished', 'matrix')

    def get_finished(self, obj):
        return obj.end_date is not None

    def get_matrix(self, obj):
        return obj.get_matrix()
