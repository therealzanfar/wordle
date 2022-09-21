# cSpell:words wordle wordlist

"""Logic for solving a Wordle puzzle"""

from importlib.resources import open_text
from typing import Optional

from wordle import WORDLIST_FILENAME, AbstractUI, GuessResult
from wordle.wordlist import Wordlist


class Solver:
    """Contains logic to solve a Wordle puzzle"""

    def __init__(
        self, ui: AbstractUI, wordlist: Optional[Wordlist] = None
    ) -> None:
        self._ui = ui
        self._wordlist = wordlist or Wordlist.from_csv(
            open_text("wordle", WORDLIST_FILENAME)
        )

    def start(self) -> None:
        """Start the solving process"""

        self._ui.welcome()
        while True:
            guess = self._wordlist.guess
            results = self._ui.show_guess(guess)

            for pos, (result, letter) in enumerate(zip(results, guess)):

                if result is GuessResult.CORRECT:
                    self._wordlist.solution(pos, letter)
                    continue

                if result is GuessResult.MISPLACED:
                    self._wordlist.present(letter)
                    self._wordlist.silenced(pos, letter)
                    continue

                if result is GuessResult.MISSING:
                    self._wordlist.missing(letter)
                    continue

                raise TypeError(f"Unknown result {result}")

            if self._wordlist.solved:
                break
