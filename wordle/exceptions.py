# cSpell:words wordle

"""Custom Error Types"""


class WordleError(Exception):
    """Parent Error Type"""


class NoWordsFoundError(WordleError):
    """No words found that match the criteria"""

    def __init__(self, message: str = None, **kwargs: object) -> None:
        message = message or "No words match the current criteria"
        super().__init__(message, **kwargs)


class FilterError(WordleError):
    """Generic error for filtering issues"""


class RedundantFilterError(FilterError):
    """Adding a filter that matches or is a subset of existing filters"""

    def __init__(self, message: str = None, **kwargs: object) -> None:
        message = (
            message
            or "Filter criteria is redundant or has already been specified"
        )
        super().__init__(message, **kwargs)


class ContradictoryFilterError(FilterError):
    """Adding a filter that conflicts with existing filters"""

    def __init__(self, message: str = None, **kwargs: object) -> None:
        message = message or "Filter criteria conflicts with existing filters"
        super().__init__(message, **kwargs)
