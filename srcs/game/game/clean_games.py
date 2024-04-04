from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from game_matchmaking.models import Game


class Command(BaseCommand):
    help = 'Clean games'

    MAX_WAIT = 120

    def handle(self, *args, **options):

        old_games = Game.objects.filter(status=Game.GameStatus.WAITING).filter(connection_time__lt=timezone.now() - timedelta(seconds=self.MAX_WAIT))

        for game in old_games:
            game.delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned games'))
