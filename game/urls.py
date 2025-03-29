from django.urls import path
from .views import StartGameView, GuessWordView, LeaderboardView, UserStatsView
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path('start/', StartGameView.as_view(), name='start-game'),
    path('guess/<int:game_id>/', GuessWordView.as_view(), name='guess-word'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
]
