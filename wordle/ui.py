# cSpell:words wordle wordlist

"""UI Modules"""

from wordle import AbstractUI, GuessResponse, GuessResult


class TextUI(AbstractUI):
    """UI Module for a test-based interface"""

    def welcome(self) -> None:
        print("Welcome to the Wordle solver")
        print()

    def show_guess(self, guess: str) -> GuessResponse:
        results = [GuessResult.MISSING for _ in guess]

        print(f"Best guess: {guess.upper():s}")
        response = self._get_user_response(guess)

        for pos, expected in enumerate(response):
            if expected.isupper():
                results[pos] = GuessResult.CORRECT
                continue

            if expected.islower():
                results[pos] = GuessResult.MISPLACED
                continue

            results[pos] = GuessResult.MISSING

        return tuple(results)

    def _get_user_response(self, guess: str) -> str:

        print("Enter the results:")
        print("- Use upper-case for correct letters")
        print("- User lower-case for misplaced letters")
        print("- leave incorrect letters blank")

        raw = "     "
        while True:
            raw = input("> ")

            if len(raw) != len(guess):
                print("Incorrect number of characters, please try again")
                continue

            if any(
                r.isalpha() and r.upper() != g.upper()
                for r, g in zip(raw, guess)
            ):
                print("Invalid entry, please try again")
                continue

            break

        return raw
