from django.test import TestCase
from django.contrib.auth.models import User
from .models import WordList, Game, Leaderboard
from .utils import check_guess  # type: ignore # assuming you put the check_guess function in utils.py


class CheckGuessTestCase(TestCase):
    def test_all_correct(self):
        self.assertEqual(check_guess("apple", "apple"), "GGGGG")

    def test_all_incorrect(self):
        self.assertEqual(check_guess("apple", "zzzzz"), "XXXXX")

    def test_some_yellow(self):
        # 'p' and 'l' are in the word but wrong places
        self.assertEqual(check_guess("apple", "plaza"), "YYXGX")

    def test_repeated_letters(self):
        # actual word has one 'p', guess has two 'p's
        self.assertEqual(check_guess("apple", "ppppp"), "GXXXY")

class WordListModelTestCase(TestCase):
    def setUp(self):
        self.word = WordList.objects.create(word="apple", language="en", word_length=5)

    def test_word_creation(self):
        self.assertEqual(self.word.word, "apple")
        self.assertEqual(self.word.language, "en")
        self.assertEqual(self.word.word_length, 5)

class GameModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.word = WordList.objects.create(word="apple", language="en", word_length=5)
        self.game = Game.objects.create(user=self.user, word=self.word)

    def test_game_creation(self):
        self.assertEqual(self.game.user.username, 'testuser')
        self.assertEqual(self.game.word.word, "apple")
        self.assertTrue(self.game.is_active)

    def test_end_game_win(self):
        self.game.end_game("win")
        self.game.refresh_from_db()
        self.assertFalse(self.game.is_active)
        self.assertEqual(self.game.result, "win")

class LeaderboardModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
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
