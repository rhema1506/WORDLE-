from django.urls import path
from .views import StartGame, MakeGuess, GameStatus, WordStatsView

urlpatterns = [
    path('start/', StartGame.as_view(), name='start-game'),
    path('guess/<int:game_id>/', MakeGuess.as_view(), name='make-guess'),
    path('status/<int:game_id>/', GameStatus.as_view(), name='game-status'),
    path('stats/', WordStatsView.as_view(), name='word-stats'),
]
