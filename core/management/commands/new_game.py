from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from core.models import Game


class Command(BaseCommand):
    help = 'Create new game'

    def add_arguments(self, parser):
        parser.add_argument('width', type=int)
        parser.add_argument('height', type=int)
        parser.add_argument('mines', type=int)

    def handle(self, *args, **options):
        game = Game.objects.create(
            user=User.objects.first(),
            width=int(options['width']),
            height=int(options['height']),
            mines=int(options['mines']),
        )
