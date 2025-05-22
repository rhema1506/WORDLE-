from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class WordBase(models.Model):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ru', 'Russian'),
    ]

    word = models.CharField(max_length=6, unique=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    class Meta:
        abstract = True

    def __str__(self):
        return self.word


class Word4(WordBase):
    def save(self, *args, **kwargs):
        if len(self.word) != 4:
            raise ValueError("Word must be exactly 4 letters")
        super().save(*args, **kwargs)


class Word5(WordBase):
    def save(self, *args, **kwargs):
        if len(self.word) != 5:
            raise ValueError("Word must be exactly 5 letters")
        super().save(*args, **kwargs)


class Word6(WordBase):
    def save(self, *args, **kwargs):
        if len(self.word) != 6:
            raise ValueError("Word must be exactly 6 letters")
        super().save(*args, **kwargs)


class Game(models.Model):
    RESULT_CHOICES = [
        ('win', 'Win'),
        ('lose', 'Lose'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word_length = models.PositiveSmallIntegerField()
    language = models.CharField(max_length=2, choices=WordBase.LANGUAGE_CHOICES, default='en')
    word4 = models.ForeignKey(Word4, null=True, blank=True, on_delete=models.SET_NULL)
    word5 = models.ForeignKey(Word5, null=True, blank=True, on_delete=models.SET_NULL)
    word6 = models.ForeignKey(Word6, null=True, blank=True, on_delete=models.SET_NULL)
    guesses = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, blank=True, choices=RESULT_CHOICES)
    trophy = models.CharField(max_length=100, blank=True)  # <-- Added trophy field

    def __str__(self):
        return f"{self.user.username} - {self.get_word()} - {self.result or 'in progress'}"

    def get_word(self):
        if self.word_length == 4 and self.word4:
            return self.word4.word
        elif self.word_length == 5 and self.word5:
            return self.word5.word
        elif self.word_length == 6 and self.word6:
            return self.word6.word
        return None

    def end_game(self, result):
        self.is_active = False
        self.finished_at = timezone.now()
        self.result = result

        leaderboard, _ = Leaderboard.objects.get_or_create(user=self.user)
        leaderboard.total_games += 1

        if result == 'win':
            leaderboard.total_wins += 1
            leaderboard.current_streak += 1
            leaderboard.longest_streak = max(leaderboard.longest_streak, leaderboard.current_streak)

            # Assign trophy based on guesses and streak
            guess_count = len(self.guesses or [])
            if guess_count <= 2:
                self.trophy = "Genius 🧠"
            elif leaderboard.current_streak >= 10:
                self.trophy = "Gold Streak 🥇"
            elif leaderboard.current_streak >= 5:
                self.trophy = "Silver Streak 🥈"
            else:
                self.trophy = "Winner 🏆"
        else:
            leaderboard.current_streak = 0
            self.trophy = "Try Again 💔"

        leaderboard.save()
        self.save()

    @staticmethod
    def create_new_game(user, language='en', length=5):
        word_obj = None
        if length == 4:
            word_obj = Word4.objects.filter(language=language).order_by('?').first()
            return Game.objects.create(user=user, word_length=4, language=language, word4=word_obj)
        elif length == 5:
            word_obj = Word5.objects.filter(language=language).order_by('?').first()
            return Game.objects.create(user=user, word_length=5, language=language, word5=word_obj)
        elif length == 6:
            word_obj = Word6.objects.filter(language=language).order_by('?').first()
            return Game.objects.create(user=user, word_length=6, language=language, word6=word_obj)
        else:
            raise ValueError("Invalid word length")


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
