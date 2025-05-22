from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.http import HttpResponse
from django.apps import apps
import json

# Models
Word4 = apps.get_model('game', 'Word4')
Word5 = apps.get_model('game', 'Word5')
Word6 = apps.get_model('game', 'Word6')
Game = apps.get_model('game', 'Game')
Leaderboard = apps.get_model('game', 'Leaderboard')

# Serializers
from .serializers import GameSerializer, LeaderboardSerializer


def home(request):
    return HttpResponse("Welcome to the Wordle API!")


def generate_feedback(guess, correct_word):
    feedback = ['grey'] * len(guess)
    correct_word_chars = list(correct_word)

    # First pass - green
    for i, letter in enumerate(guess):
        if letter == correct_word[i]:
            feedback[i] = 'green'
            correct_word_chars[i] = None

    # Second pass - yellow
    for i, letter in enumerate(guess):
        if feedback[i] == 'green':
            continue
        if letter in correct_word_chars:
            feedback[i] = 'yellow'
            correct_word_chars[correct_word_chars.index(letter)] = None

    return feedback


class StartGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        length = int(request.data.get('length', 5))
        language = request.data.get('language', 'en')

        if length not in [4, 5, 6]:
            return Response({'error': 'Length must be 4, 5 or 6'}, status=400)

        game = Game.create_new_game(user=request.user, language=language, length=length)
        if not game:
            return Response({'error': 'Could not create game'}, status=500)

        serializer = GameSerializer(game)
        data = serializer.data
        data['max_guesses'] = 6
        return Response(data)


class GuessWordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        guess = request.data.get('guess', '').lower()
        game = Game.objects.filter(id=game_id, user=request.user, is_active=True).first()

        if not game:
            return Response({'error': 'Active game not found'}, status=404)

        word = game.get_word()

        if not guess.isalpha():
            return Response({'error': 'Guess must contain only letters'}, status=400)

        if len(guess) != len(word):
            return Response({'error': f'Guess must be a {len(word)}-letter word'}, status=400)

        feedback = generate_feedback(guess, word)

        if isinstance(game.guesses, str):
            try:
                game.guesses = json.loads(game.guesses)
            except json.JSONDecodeError:
                game.guesses = []

        game.guesses.append({'guess': guess, 'feedback': feedback})

        if guess == word:
            game.end_game('win')
        elif len(game.guesses) >= 6:
            game.end_game('lose')
        else:
            game.save()

        serializer = GameSerializer(game)
        return Response(serializer.data)


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaderboard = Leaderboard.objects.order_by('-longest_streak')[:10]
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
        serializer = LeaderboardSerializer(leaderboard)
        return Response(serializer.data)


class ActiveGameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        game = Game.objects.filter(user=request.user, is_active=True).last()
        if not game:
            return Response({'active': False})

        serializer = GameSerializer(game)
        return Response({'active': True, 'game': serializer.data})
