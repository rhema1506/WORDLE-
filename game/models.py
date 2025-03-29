from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


class WordList(models.Model):  # Ensure this exists
    word = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.word

    @staticmethod
    def get_random_word():
        """Fetch a random word from the database."""
        words = WordList.objects.all()
        return random.choice(word) if word.exists() else None


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    guesses = models.JSONField(default=list)  
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, blank=True, choices=[("win", "Win"), ("lose", "Lose")])

    def __str__(self):
        return f"{self.user.username} - {self.word.text} - {self.result}"

    def end_game(self, result):
        """Ends the game and updates the leaderboard."""
        self.is_active = False
        self.finished_at = timezone.now()
        self.result = result
        self.save()

        # Update Leaderboard
        leaderboard, created = Leaderboard.objects.get_or_create(user=self.user)
        leaderboard.total_games += 1
        if result == "win":
            leaderboard.total_wins += 1
            leaderboard.current_streak += 1
            leaderboard.longest_streak = max(leaderboard.longest_streak, leaderboard.current_streak)
        else:
            leaderboard.current_streak = 0  # Reset streak on loss
        leaderboard.save()

    @staticmethod
    def create_new_game(user):
        """Creates a new game for a user with a random word."""
        word = Wordlist.get_random_word()
        if word:
            return Game.objects.create(user=user, word=word)
        return None


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s stats"

    @property
    def win_ratio(self):
        """Returns the win percentage."""
        return (self.total_wins / self.total_games) * 100 if self.total_games > 0 else 0
