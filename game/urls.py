from django.urls import path
from .views import (
    home,
    StartGameView,
    GuessWordView,
    LeaderboardView,
    UserStatsView
)

app_name = "game"

urlpatterns = [
    path('', home, name='home'),
    path('api/start/', StartGameView.as_view(), name='start-game'),
    path('api/guess/<int:game_id>/', GuessWordView.as_view(), name='guess-word'),
    path('api/leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('api/stats/', UserStatsView.as_view(), name='user-stats'),
]
