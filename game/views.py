from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Word, Game, Leaderboard
from .serializers import GameSerializer, LeaderboardSerializer
import random


def generate_feedback(guess, correct_word):
    feedback = []
    for idx, letter in enumerate(guess):
        if letter == correct_word[idx]:
            feedback.append('green')
        elif letter in correct_word:
            feedback.append('yellow')
        else:
            feedback.append('grey')
    return feedback


class StartGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Select a random word for the game
        word = random.choice(Word.objects.all())
        game = Game.objects.create(user=request.user, word=word)
        return Response({'message': 'Game started', 'game_id': game.id})


class GuessWordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        guess = request.data.get('guess', '').lower()
        if len(guess) != 5:
            return Response({'error': 'Guess must be a 5-letter word'}, status=400)

        game = Game.objects.filter(id=game_id, user=request.user, is_active=True).first()
        if not game:
            return Response({'error': 'Active game not found'}, status=404)

        feedback = generate_feedback(guess, game.word.text)
        game.guesses.append({'guess': guess, 'feedback': feedback})
        
        if guess == game.word.text:
            game.is_active = False
            game.result = 'win'
            game.finished_at = timezone.now()

            leaderboard, created = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard.total_games += 1
            leaderboard.total_wins += 1
            leaderboard.current_streak += 1
            leaderboard.longest_streak = max(leaderboard.longest_streak, leaderboard.current_streak)
            leaderboard.save()

        elif len(game.guesses) >= 6:
            game.is_active = False
            game.result = 'lose'
            game.finished_at = timezone.now()

            leaderboard, created = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard.total_games += 1
            leaderboard.current_streak = 0
            leaderboard.save()

        game.save()

        return Response({
            'feedback': feedback,
            'result': game.result,
            'guesses': game.guesses,
            'remaining_guesses': 6 - len(game.guesses)
        })


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaderboard = Leaderboard.objects.order_by('-longest_streak')[:10]
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaderboard, created = Leaderboard.objects.get_or_create(user=request.user)
        serializer = LeaderboardSerializer(leaderboard)
        return Response(serializer.data)
