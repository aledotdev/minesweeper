from django.shortcuts import render, redirect
from django.views import View
from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Game


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['width', 'height', 'mines']


def game_view(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'game.html', {'game': game})


def game_list_view(request):
    games = Game.objects.order_by('-id')[0:20]
    return render(request, 'games_list.html', {'games': games})


class NewGameView(View):
    def get(self, request):
        return render(request, 'new_game.html', {'form': GameForm()})

    def post(self, request, *args, **kwargs):
        form = GameForm(request.POST)
        if form.is_valid():
            game = Game(**form.cleaned_data)
            game.user = User.objects.first()
            game.save()

            return redirect('/game/{}/'.format(game.id))
