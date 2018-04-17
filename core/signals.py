from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Game


@receiver(post_save, sender=Game)
def generate_new_game(sender, instance, created, **kwargs):
    if created:
        instance.new_board()


@receiver(post_save, sender=Game)
def check_mines_avg(sender, instance, **kwargs):
    instance.too_much_mines(raise_except=True)
