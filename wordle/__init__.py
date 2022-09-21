# cSpell:words Wyant wordle wordlist

"""Wordle Solver"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from multiprocessing.util import abstract_sockets_supported
from typing import NamedTuple

__author__ = """Matthew Wyant"""
__email__ = "me@matthewwyant.com"
__copyright__ = "Copyright 2022, Matthew Wyant"
__credits__ = [__author__]
__license__ = "GPL-3.0-plus"
__version__ = "0.1.0"
__version_info__ = (0, 1, 0)
__maintainer__ = __author__
__status__ = "Prototype"

WORD_LEN = 5
WORDLIST_FILENAME = "wordlist.csv"


class WordRecord(NamedTuple):
    """A word's data record"""

    frequency: int
    word: str

    def _cmp(self, other) -> int:
        if self.frequency < other.frequency:
            return 1  # Default reverse sort on frequency
        if self.frequency > other.frequency:
            return -1  # Default reverse sort on frequency
        if self.word > other.word:
            return 1
        if self.word < other.word:
            return -1
        return 0

    def __eq__(self, other) -> bool:
        return self._cmp(other) == 0

    def __ne__(self, other) -> bool:
        return self._cmp(other) != 0

    def __gt__(self, other) -> bool:
        return self._cmp(other) == 1

    def __lt__(self, other) -> bool:
        return self._cmp(other) == -1

    def __ge__(self, other) -> bool:
        return self._cmp(other) >= 0

    def __le__(self, other) -> bool:
        return self._cmp(other) <= 0


class GuessResult(Enum):
    """Per-character results of a Wordle guess"""

    CORRECT = auto()
    MISPLACED = auto()
    MISSING = auto()


GuessResponse = tuple[GuessResult, ...]


class AbstractUI(ABC):
    """Abstract class for UI modules"""

    @abstractmethod
    def welcome(self) -> None:
        """Welcome the user to the game"""

    @abstractmethod
    def show_guess(self, guess: str) -> GuessResponse:
        """Show the user a guess and prompt for a response"""
