from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Leaderboard, WordList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordList
        fields = ('id', 'word', 'language', 'word_length')


class GameSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    word = WordListSerializer(read_only=True)
    result = serializers.ChoiceField(choices=Game.RESULT_CHOICES, required=False)

    class Meta:
        model = Game
        fields = [
            'id', 'user', 'word', 'guesses', 'is_active',
            'started_at', 'finished_at', 'result'
        ]
        read_only_fields = ('started_at', 'finished_at', 'is_active', 'result')

    def create(self, validated_data):
        user = self.context['request'].user
        # You may want to handle creating a new Game here or override elsewhere
        return Game.create_new_game(user=user)  # Assumes create_new_game returns a Game instance


class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    win_ratio = serializers.FloatField(source='win_ratio', read_only=True)

    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user', 'total_games', 'total_wins',
            'current_streak', 'longest_streak', 'win_ratio'
        ]
        read_only_fields = fields  # Make all leaderboard fields read-only, updated internally
