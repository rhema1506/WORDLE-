from django.contrib import admin
from .models import WordList, Game, Leaderboard  

class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'word', 'is_active', 'result', 'finished_at')  # Updated fields
    search_fields = ('user__username', 'word__text')  # Ensure related field lookup

class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_games', 'total_wins', 'current_streak', 'longest_streak')  # Updated fields
    search_fields = ('user__username',)

admin.site.register(WordList)
admin.site.register(Game, GameAdmin)
admin.site.register(Leaderboard, LeaderboardAdmin)
