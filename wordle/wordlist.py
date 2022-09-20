"""Code related to wordlist storage and filtering"""

from typing import Iterable, Optional

from wordle import WORD_LEN
from wordle.exceptions import (
    NoWordsFoundError,
    RedundantFilterError,
    ContradictoryFilterError,
)


class Wordlist:
    """Object for word list storage and filtering"""

    def __init__(
        self,
        word_length: Optional[int] = None,
        wordlist: Optional[Iterable[str]] = None,
    ) -> None:
        self._word_length = word_length or WORD_LEN

        self._words: list[str]
        self._filtered: list[str]
        self._modified: bool

        self._missing: set[str]
        self._present: set[str]

        self._solution: list[str | None]
        self._silenced: list[set[str]]

        self._words = []
        if wordlist is not None:
            self._load_wordlist(wordlist)
        self._reset()

    def _load_wordlist(self, wordlist: Iterable[str]) -> None:
        self._words = list(wordlist)

    def _reset(self) -> None:
        self._filtered = self._words.copy()
        self._modified = False

        self._missing = set()
        self._present = set()

        self._solution = [None for _ in range(self._word_length)]
        self._silenced = [set() for _ in range(self._word_length)]

    def _filter(self, force: bool = False) -> None:
        if self._modified or force:
            self._filtered = [
                word for word in self._filtered if self.match(word)
            ]
            self._modified = False

    def match(self, word: str) -> bool:
        """Does a word match the current criteria"""

        if self._missing and any(missing in word for missing in self._missing):
            return False

        if self._present and not any(
            present in word for present in self._present
        ):
            return False

        for pos, solution in enumerate(self._solution):
            if solution is not None and word[pos] != solution:
                return False

        for pos, silenced_chars in enumerate(self._silenced):
            if any(silenced == word[pos] for silenced in silenced_chars):
                return False

        return True

    def missing(self, letter: str) -> None:
        """Mark a letter as missing from the word"""

        if letter in self._present:
            raise ContradictoryFilterError()

        if letter in self._missing:
            raise RedundantFilterError()

        self._missing.add(letter)
        self._modified = True

    def present(self, letter: str) -> None:
        """Mark a letter as present in the word"""

        if letter in self._missing:
            raise ContradictoryFilterError()

        if letter in self._present:
            raise RedundantFilterError()

        self._present.add(letter)
        self._modified = True

    def solution(self, pos: int, letter: str) -> None:
        """Mark a letter as the solution to a character position"""

        if self._solution[pos] is not None:
            raise ContradictoryFilterError(
                "Solution at that position has already been set"
            )

        if letter in self._missing:
            raise ContradictoryFilterError()

        if self._solution[pos] == letter:
            raise RedundantFilterError()

        self._solution[pos] = letter
        self._present.discard(letter)
        self._modified = True

    def silenced(self, pos: int, letter: str) -> None:
        """Mark a letter as the not-a-solution to a character position"""

        if self._solution[pos] == letter:
            raise ContradictoryFilterError()

        if letter in self._missing:
            raise RedundantFilterError()

        if letter in self._silenced[pos]:
            raise RedundantFilterError()

        self._silenced[pos].add(letter)
        self._modified = True

    @property
    def guess(self) -> str:
        """Return the best word guess"""

        self._filter()

        try:
            return self._filtered[0]
        except IndexError as e:
            raise NoWordsFoundError() from e
