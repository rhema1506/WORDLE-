from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Leaderboard, Word4, Word5, Word6


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class Word4Serializer(serializers.ModelSerializer):
    class Meta:
        model = Word4
        fields = ('id', 'word', 'language')


class Word5Serializer(serializers.ModelSerializer):
    class Meta:
        model = Word5
        fields = ('id', 'word', 'language')


class Word6Serializer(serializers.ModelSerializer):
    class Meta:
        model = Word6
        fields = ('id', 'word', 'language')


class GameSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    word = serializers.SerializerMethodField()
    result = serializers.ChoiceField(choices=Game.RESULT_CHOICES, required=False)
    trophy = serializers.CharField(read_only=True)  # 🏆 Include trophy info

    class Meta:
        model = Game
        fields = [
            'id', 'user', 'word_length', 'language',
            'word',  # custom display from get_word()
            'guesses', 'is_active', 'started_at', 'finished_at',
            'result', 'trophy'  # 🏆 Add trophy here
        ]
        read_only_fields = (
            'user', 'word', 'is_active', 'started_at',
            'finished_at', 'result', 'trophy'  # Make trophy read-only
        )

    def get_word(self, obj):
        # Only return the word if the game is finished
        return obj.get_word() if not obj.is_active else None

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None

        language = validated_data.get('language', 'en')
        length = validated_data.get('word_length', 5)

        return Game.create_new_game(user=user, language=language, length=length)


class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    win_ratio = serializers.FloatField(read_only=True)

    class Meta:
        model = Leaderboard
        fields = [
            'id', 'user', 'total_games', 'total_wins',
            'current_streak', 'longest_streak', 'win_ratio'
        ]
        read_only_fields = fields
