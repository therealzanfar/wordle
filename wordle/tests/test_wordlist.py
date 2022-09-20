"""Test the wordlist object"""

import pytest

from wordle.wordlist import Wordlist
from wordle.exceptions import NoWordsFoundError


DEF_WORDLIST = [
    "about",
    "other",
    "which",
    "their",
    "there",
    "first",
    "would",
    "these",
]


def test_creation():
    wordlist = Wordlist()

    with pytest.raises(NoWordsFoundError):
        _ = wordlist.guess


def test_population_init():
    wordlist = Wordlist(wordlist=DEF_WORDLIST)

    assert wordlist.guess == "about"


def test_missing_chars():
    wordlist = Wordlist(wordlist=DEF_WORDLIST)
    wordlist.missing("a")

    assert wordlist.guess == "other"


def test_present_chars():
    wordlist = Wordlist(wordlist=DEF_WORDLIST)
    wordlist.present("i")

    assert wordlist.guess == "which"


def test_solution_chars():
    wordlist = Wordlist(wordlist=DEF_WORDLIST)
    wordlist.solution(4, "e")

    assert wordlist.guess == "there"


def test_silenced_chars():
    wordlist = Wordlist(wordlist=DEF_WORDLIST)
    wordlist.silenced(2, "o")

    assert wordlist.guess == "other"
