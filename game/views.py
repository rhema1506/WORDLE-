from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.apps import apps
import random

# Home view
def home(request):
    return HttpResponse("Welcome to the Wordle API!")

# Dynamically load models to avoid circular imports or startup issues
WordList = apps.get_model('game', 'WordList')
Game = apps.get_model('game', 'Game')
Leaderboard = apps.get_model('game', 'Leaderboard')

from .serializers import GameSerializer, LeaderboardSerializer


def generate_feedback(guess, correct_word):
    """
    Generate feedback as a list with values:
    'green'  - correct letter & position
    'yellow' - letter in word but wrong position
    'grey'   - letter not in word
    Properly handles repeated letters.
    """
    feedback = ['grey'] * len(guess)
    correct_word_chars = list(correct_word)
    
    # First pass - greens
    for i, letter in enumerate(guess):
        if letter == correct_word[i]:
            feedback[i] = 'green'
            correct_word_chars[i] = None  # mark matched
    
    # Second pass - yellows
    for i, letter in enumerate(guess):
        if feedback[i] == 'green':
            continue
        if letter in correct_word_chars:
            feedback[i] = 'yellow'
            correct_word_chars[correct_word_chars.index(letter)] = None  # mark matched
    
    return feedback


class StartGameView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get all words; consider filtering by language or length if needed
        words = list(WordList.objects.values_list('word', flat=True))
        if not words:
            return Response({'error': 'No words available in the database'}, status=500)

        word_text = random.choice(words)
        word = WordList.objects.filter(word=word_text).first()

        game = Game.objects.create(user=request.user, word=word)
        return Response({'message': 'Game started', 'game_id': game.id})


class GuessWordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, game_id):
        guess = request.data.get('guess', '').lower()

        # Validate guess length matches word length (flexible for different lengths)
        game = Game.objects.filter(id=game_id, user=request.user, is_active=True).first()
        if not game:
            return Response({'error': 'Active game not found'}, status=404)

        if len(guess) != len(game.word.word):
            return Response({'error': f'Guess must be a {len(game.word.word)}-letter word'}, status=400)

        feedback = generate_feedback(guess, game.word.word)

        # Safely load guesses list
        if isinstance(game.guesses, str):
            import json
            try:
                game.guesses = json.loads(game.guesses)
            except json.JSONDecodeError:
                game.guesses = []

        game.guesses.append({'guess': guess, 'feedback': feedback})

        if guess == game.word.word:
            game.is_active = False
            game.result = 'win'
            game.finished_at = timezone.now()

            leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard.total_games += 1
            leaderboard.total_wins += 1
            leaderboard.current_streak += 1
            leaderboard.longest_streak = max(leaderboard.longest_streak, leaderboard.current_streak)
            leaderboard.save()

        elif len(game.guesses) >= 6:
            game.is_active = False
            game.result = 'lose'
            game.finished_at = timezone.now()

            leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
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
        leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
        serializer = LeaderboardSerializer(leaderboard)
        return Response(serializer.data)
