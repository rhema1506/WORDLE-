from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.apps import apps
import random


def home(request):
    return HttpResponse("Welcome to the Wordle API!")

# Dynamically get models to avoid import issues
WordList = apps.get_model('game', 'WordList')
Game = apps.get_model('game', 'Game')
Leaderboard = apps.get_model('game', 'Leaderboard')

from .serializers import GameSerializer, LeaderboardSerializer


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
        # Ensure at least one word exists before choosing
        words = list(WordList.objects.values_list('text', flat=True))
        if not words:
            return Response({'error': 'No words available in the database'}, status=500)

        word_text = random.choice(words)
        word = WordList.objects.filter(text=word_text).first()

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

        # Ensure game.guesses is a list (handling potential JSON serialization issues)
        if isinstance(game.guesses, str):
            import json
            try:
                game.guesses = json.loads(game.guesses)
            except json.JSONDecodeError:
                game.guesses = []

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
