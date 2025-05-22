from django.contrib import admin
from .models import Game, Leaderboard, Word4, Word5, Word6


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'word_length', 'language',
        'is_active', 'result', 'started_at', 'attempts'
    ]
    readonly_fields = ['started_at', 'finished_at']

    def attempts(self, obj):
        return len(obj.guesses) if obj.guesses else 0
    attempts.short_description = "Attempts"


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total_games', 'total_wins',
        'total_losses', 'current_streak', 'longest_streak'
    ]

    def total_losses(self, obj):
        return obj.total_games - obj.total_wins
    total_losses.short_description = "Total Losses"


@admin.register(Word4)
class Word4Admin(admin.ModelAdmin):
    list_display = ['id', 'word', 'language']


@admin.register(Word5)
class Word5Admin(admin.ModelAdmin):
    list_display = ['id', 'word', 'language']


@admin.register(Word6)
class Word6Admin(admin.ModelAdmin):
    list_display = ['id', 'word', 'language']
