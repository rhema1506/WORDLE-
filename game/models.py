from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


class WordLength(models.Model):
    length = models.IntegerField()

    def __str__(self):
        return str(self.length)


class WordList(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Russian'),
    ]

    word = models.CharField(max_length=10, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    word_length = models.ForeignKey(WordLength, on_delete=models.CASCADE)
    def __str__(self):
        return self.word

    @staticmethod
    def get_random_word(language=None, length=None):
        """
        Fetch a random word optionally filtered by language and length.
        """
        queryset = WordList.objects.all()
        if language:
            queryset = queryset.filter(language=language)
        if length:
            queryset = queryset.filter(word_length__length=length)
        words = list(queryset)
        return random.choice(words) if words else None


class Game(models.Model):
    RESULT_CHOICES = [
        ('win', 'Win'),
        ('lose', 'Lose'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(WordList, on_delete=models.CASCADE)
    guesses = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, blank=True, choices=RESULT_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.word.word} - {self.result or 'in progress'}"

    def end_game(self, result):
        self.is_active = False
        self.finished_at = timezone.now()
        self.result = result
        self.save()

        leaderboard, _created = Leaderboard.objects.get_or_create(user=self.user)
        leaderboard.total_games += 1

        if result == 'win':
            leaderboard.total_wins += 1
            leaderboard.current_streak += 1
            leaderboard.longest_streak = max(leaderboard.longest_streak, leaderboard.current_streak)
        else:
            leaderboard.current_streak = 0

        leaderboard.save()

    @staticmethod
    def create_new_game(user, language=None, length=None):
        word = WordList.get_random_word(language=language, length=length)
        if word:
            return Game.objects.create(user=user, word=word)
        return None


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_games = models.PositiveIntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s stats"

    @property
    def win_ratio(self):
        return (self.total_wins / self.total_games) * 100 if self.total_games > 0 else 0
