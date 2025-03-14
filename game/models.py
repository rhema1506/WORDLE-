from django.db import models
from django.utils import timezone

class WordList(models.Model):
    word = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.word

class GameSession(models.Model):
    word_to_guess = models.ForeignKey(WordList, on_delete=models.CASCADE)
    attempts_left = models.IntegerField(default=6)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id} - Active: {self.is_active}"

class WordStats(models.Model):
    date = models.DateField(default=timezone.now)
    total_words = models.IntegerField(default=0)
    words_used_today = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date}: {self.words_used_today} used"
