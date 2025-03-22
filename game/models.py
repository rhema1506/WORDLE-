from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random

class Word(models.Model):
    text = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.text


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    guesses = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, blank=True)  # win/lose

    def __str__(self):
        return f"{self.user.username} - {self.word.text} - {self.result}"


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games = models.IntegerField(default=0)
    total_wins = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s stats"
