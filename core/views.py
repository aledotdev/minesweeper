from django.shortcuts import render

from .models import Game


def game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'game.html', {'game': game})
