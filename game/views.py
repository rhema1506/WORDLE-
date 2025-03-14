from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import WordList, GameSession, WordStats
from django.utils.timezone import now
from random import choice

def update_word_stats():
    today = now().date()
    stats, created = WordStats.objects.get_or_create(date=today)
    stats.total_words = WordList.objects.count()
    stats.save()

class StartGame(APIView):
    def post(self, request):
        update_word_stats()

        words = WordList.objects.all()
        if not words.exists():
            return Response({'error': 'No words in database!'}, status=status.HTTP_400_BAD_REQUEST)

        random_word = choice(words)
        game = GameSession.objects.create(word_to_guess=random_word)

        # Increment today's word usage
        stats = WordStats.objects.get(date=now().date())
        stats.words_used_today += 1
        stats.save()

        return Response({
            'message': 'Game started!',
            'game_id': game.id,
            'attempts_left': game.attempts_left
        })

class MakeGuess(APIView):
    def post(self, request, game_id):
        game = get_object_or_404(GameSession, id=game_id)

        if not game.is_active:
            return Response({'error': 'Game over!'}, status=status.HTTP_400_BAD_REQUEST)

        guess = request.data.get('guess', '').lower()
        if len(guess) != 5:
            return Response({'error': 'Guess must be a 5-letter word.'}, status=status.HTTP_400_BAD_REQUEST)

        correct_word = game.word_to_guess.word

        # Build response (e.g., correct position and letters)
        result = []
        for i in range(5):
            if guess[i] == correct_word[i]:
                result.append({'letter': guess[i], 'result': 'correct'})
            elif guess[i] in correct_word:
                result.append({'letter': guess[i], 'result': 'present'})
            else:
                result.append({'letter': guess[i], 'result': 'absent'})

        game.attempts_left -= 1
        if guess == correct_word:
            game.is_active = False
            message = '🎉 Congratulations! You guessed the word!'
        elif game.attempts_left <= 0:
            game.is_active = False
            message = f'❌ Game over! The word was "{correct_word}".'
        else:
            message = 'Try again!'

        game.save()

        return Response({
            'message': message,
            'result': result,
            'attempts_left': game.attempts_left,
            'game_active': game.is_active
        })

class GameStatus(APIView):
    def get(self, request, game_id):
        game = get_object_or_404(GameSession, id=game_id)

        return Response({
            'game_id': game.id,
            'attempts_left': game.attempts_left,
            'is_active': game.is_active,
            'created_at': game.created_at
        })

class WordStatsView(APIView):
    def get(self, request):
        stats = WordStats.objects.all().order_by('-date')[:7]
        data = [{
            'date': s.date,
            'total_words': s.total_words,
            'words_used_today': s.words_used_today
        } for s in stats]

        return Response(data)
