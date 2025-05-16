from django.contrib import admin
from .models import WordList, Game, Leaderboard, WordLength

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'word', 'is_active', 'result', 'finished_at')
    search_fields = ('user__username', 'word__word')
    list_filter = ('is_active', 'result', 'finished_at')
    ordering = ('-finished_at',)

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_games', 'total_wins', 'current_streak', 'longest_streak')
    search_fields = ('user__username',)
    ordering = ('-total_wins',)

@admin.register(WordList)
class WordListAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'word_length')
    search_fields = ('word',)
    list_filter = ('word_length',)

@admin.register(WordLength)
class WordLengthAdmin(admin.ModelAdmin):
    list_display = ('id', 'length')
