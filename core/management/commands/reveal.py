from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from core.models import Game


class Command(BaseCommand):
    help = 'Display matrix game'

    def add_arguments(self, parser):
        parser.add_argument('game', type=int)
        parser.add_argument('x', type=int)
        parser.add_argument('y', type=int)

    def handle(self, *args, **options):
        x = options['x']
        y = options['y']

        game = Game.objects.get(id=options['game'])

        game.reveal(options['x'], options['y'])

        for r in game.get_neighboors(x, y):
            print(r)

        print(game.count_neighbors_mines(x, y))
