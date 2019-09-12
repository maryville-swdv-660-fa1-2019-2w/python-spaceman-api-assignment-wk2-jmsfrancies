from django.test import TestCase
from game_api.models import Game

from django.core.exceptions import ValidationError


class GameModelTests(TestCase):

    # word field
    def test_init_should_assign_given_word(self):
        game = Game(word="TESTWORD")
        self.assertEquals(game.word, "TESTWORD")

    def test_word_is_required(self):
        with self.assertRaises(ValidationError):
            game = Game()
            game.full_clean()

    def test_word_is_less_than_3_chars(self):
        with self.assertRaises(ValidationError):
            game = Game(word="AA")
            game.full_clean()

    def test_word_is_only_letters(self):
        with self.assertRaises(ValidationError):
            game = Game(word="A1B")
            game.full_clean()

    # guesses_taken field

    def test_guesses_taken_should_not_increment_if_letter_in_word(self):
        expectedGuessesTaken = 2
        game = Game(
            word='TESTWORD',
            guessed_word_state=['', '', 'S', '', 'W', 'O', 'R', ''],
            letters_guessed=['S', 'A', 'W', 'O', 'R', 'C'],
            guesses_allowed=5,
            guesses_taken=expectedGuessesTaken
        )

        game.handleGuess('T')
        self.assertEquals(expectedGuessesTaken, game.guesses_taken)

    def test_guesses_taken_should_increment_if_letter_not_in_word(self):
        expectedGuessesTaken = 2
        game = Game(
            word='TESTWORD',
            guessed_word_state=['', '', 'S', 'A', 'W', 'O', 'R', ''],
            letters_guessed=['S', 'A', 'W', 'O', 'R', 'C'],
            guesses_allowed=5,
            guesses_taken=expectedGuessesTaken
        )

        game.handleGuess('X')
        self.assertNotEquals(expectedGuessesTaken, game.guesses_taken)

    # guessed_word_state field
    def test_guessed_word_state_is_unchanged_if_guess_not_in_word(self):
        initialGuessedWordState = ['', '', 'S', '', 'W', 'O', 'R', '']
        game = Game(
            word='TESTWORD',
            guessed_word_state=initialGuessedWordState,
            letters_guessed=['S', 'A', 'W', 'O', 'R', 'C'],
            guesses_allowed=5,
            guesses_taken=2
        )

        game.handleGuess('X')
        self.assertEquals(initialGuessedWordState, game.guessed_word_state)

    def test_guessed_word_state_is_updated_with_guessed_letter_in_word(self):
        initialGuessedWordState = ['', '', 'S', '', 'W', 'O', 'R', '']
        expectedGuessedWordState = ['T', '', 'S', 'T', 'W', 'O', 'R', '']
        game = Game(
            word='TESTWORD',
            guessed_word_state=initialGuessedWordState,
            letters_guessed=['S', 'A', 'W', 'O', 'R', 'C'],
            guesses_allowed=5,
            guesses_taken=2
        )

        game.handleGuess('T')
        self.assertEquals(expectedGuessedWordState, game.guessed_word_state)

    # available_letters field
    def test_init_should_set_letters_available_to_alphabet(self):
        game = Game(word="TESTWORD")
        self.assertEquals(game.letters_available,
                          list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    def test_available_letters_should_remove_guessed_letters_when_letter_in_word(self):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game(
            word='TESTWORD',
            guessed_word_state=['', '', 'S', '', 'W', 'O', 'R', ''],
            letters_guessed=['S', 'A', 'W', 'O', 'R', 'C'],
            letters_available=initialLettersAvailable,
            guesses_allowed=5,
            guesses_taken=2
        )

        guess = 'T'

        game.handleGuess(guess)
        expectedLettersAvailable = [
            letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals(game.letters_available, expectedLettersAvailable)

    def test_available_letters_should_remove_guessed_letters_when_letter_not_in_word(self):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game(
            word='TESTWORD',
            guessed_word_state=['', '', 'S', '', 'W', 'O', 'R', ''],
            letters_guessed=['S', 'A', 'W', 'O', 'R', 'C'],
            letters_available=initialLettersAvailable,
            guesses_allowed=5,
            guesses_taken=2
        )

        guess = 'Q'

        game.handleGuess(guess)
        expectedLettersAvailable = [
            letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals(game.letters_available, expectedLettersAvailable)

    # letters_guessed field
    def test_letters_guessed_should_add_guessed_letter_when_letter_in_word(self):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R', 'C']
        game = Game(
            word='TESTWORD',
            guessed_word_state=['', '', 'S', '', 'W', 'O', 'R', ''],
            letters_guessed=initialLettersGuessed.copy(),
            guesses_allowed=5,
            guesses_taken=2
        )

        guess = 'T'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals(game.letters_guessed, expectedLettersGuessed)

    def test_letters_guessed_should_add_guessed_letter_when_letter_not_in_word(self):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R', 'C']
        game = Game(
            word='TESTWORD',
            guessed_word_state=['', '', 'S', '', 'W', 'O', 'R', ''],
            letters_guessed=initialLettersGuessed.copy(),
            guesses_allowed=5,
            guesses_taken=2
        )

        guess = 'Q'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals(game.letters_guessed, expectedLettersGuessed)

    # is_game_over field
    # TODO: add tests
    # HINT: considering adding a fixture or other widely scoped variables if you feel ]hat will
    #  make this easier


# This test makes sure that the is game over variable returns with false if and only if the guesses left are greater than zero


    def test_is_game_over_is_false_if_guesses_left(self):
        game = Game(
            guesses_allowed=5,
            guesses_taken=4,
            is_game_over=False
        )
        isGameFinished = game.is_game_over
        guesses_left = game.guesses_allowed - game.guesses_taken
        if guesses_left > 0:
            self.assertEquals(isGameFinished, False)
        else:
            self.assertEquals(isGameFinished, True)
#

    def test_is_game_over_is_false_if_not_all_letters_guessed(self):
        testword = "HELLO"
        total = ''
        game = Game(
            letters_guessed=['H', 'E', 'L'],
            is_game_over=False
        )
        for i in game.letters_guessed:
            total = total + i

        if testword != total:
            isGameFinished = game.is_game_over
            self.assertEquals(isGameFinished, False)

        else:
            self.assertNotEquals(isGameFinished, True)

    def test_is_game_over_is_true_if_no_guesses_left(self):
        game = Game(
            guesses_allowed=5,
            guesses_taken=5,
            is_game_over=True
        )
        isGameFinished = game.is_game_over
        self.assertEquals(isGameFinished, True)

    def test_is_game_over_is_true_if_all_letters_guessed(self):
        WordToGuess = 'HELLO'
        total = ''
        game = Game(
            letters_guessed=['H', 'E', 'L', 'L', 'O'],
            is_game_over=True
        )
        IsGameFinished = game.is_game_over

        for j in game.letters_guessed:
            total = total + j

        if total == WordToGuess:
            self.assertEquals(IsGameFinished, True)
