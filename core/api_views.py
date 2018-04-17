from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(methods=['post'], detail=True)
    def reveal(self, request, pk=None):
        game = self.get_object()
        x = int(request.data['x'])
        y = int(request.data['y'])

        game.reveal(x, y)

        serializer = self.get_serializer(game)
        return Response(serializer.data)
