from django.test import TestCase
from django.contrib.auth.models import User
from .models import Word4, Word5, Word6, Game, Leaderboard
from .utils import check_guess # type: ignore


class CheckGuessTestCase(TestCase):
    def test_all_correct(self):
        self.assertEqual(check_guess("apple", "apple"), "GGGGG")

    def test_all_incorrect(self):
        self.assertEqual(check_guess("apple", "zzzzz"), "XXXXX")

    def test_some_yellow(self):
        self.assertEqual(check_guess("apple", "plaza"), "YYXGX")

    def test_repeated_letters(self):
        self.assertEqual(check_guess("apple", "ppppp"), "GXYXX")


class GameModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.word5 = Word5.objects.create(word="apple", language="en")
        self.game = Game.objects.create(user=self.user, word_length=5, language='en', word5=self.word5)

    def test_game_creation(self):
        self.assertEqual(self.game.user.username, 'testuser')
        self.assertEqual(self.game.get_word(), "apple")
        self.assertTrue(self.game.is_active)

    def test_end_game_win(self):
        self.game.end_game("win")
        self.game.refresh_from_db()
        self.assertFalse(self.game.is_active)
        self.assertEqual(self.game.result, "win")

    def test_end_game_lose(self):
        self.game.end_game("lose")
        self.game.refresh_from_db()
        self.assertFalse(self.game.is_active)
        self.assertEqual(self.game.result, "lose")


class LeaderboardModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.word5 = Word5.objects.create(word="apple", language="en")
        self.leaderboard = Leaderboard.objects.create(user=self.user)

    def test_leaderboard_initial(self):
        self.assertEqual(self.leaderboard.total_games, 0)
        self.assertEqual(self.leaderboard.total_wins, 0)
        self.assertEqual(self.leaderboard.current_streak, 0)
        self.assertEqual(self.leaderboard.longest_streak, 0)

    def test_win_ratio(self):
        self.leaderboard.total_games = 10
        self.leaderboard.total_wins = 7
        self.leaderboard.save()
        self.assertEqual(self.leaderboard.win_ratio, 70.0)

    def test_streak_update_win(self):
        game = Game.objects.create(user=self.user, word_length=5, language='en', word5=self.word5)
        game.end_game("win")

        self.leaderboard.refresh_from_db()
        self.assertEqual(self.leaderboard.total_games, 1)
        self.assertEqual(self.leaderboard.total_wins, 1)
        self.assertEqual(self.leaderboard.current_streak, 1)
        self.assertEqual(self.leaderboard.longest_streak, 1)

    def test_streak_reset_on_loss(self):
        game = Game.objects.create(user=self.user, word_length=5, language='en', word5=self.word5)
        game.end_game("lose")

        self.leaderboard.refresh_from_db()
        self.assertEqual(self.leaderboard.current_streak, 0)
        self.assertEqual(self.leaderboard.total_games, 1)
