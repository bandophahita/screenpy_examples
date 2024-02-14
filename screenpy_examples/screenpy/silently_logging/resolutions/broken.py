from __future__ import annotations

from typing import TYPE_CHECKING, Any

from screenpy import beat

if TYPE_CHECKING:
    from hamcrest.core.base_matcher import Matcher


class IsEqualButRaisesException:
    """Resolution that raises an exception"""

    def describe(self) -> str:
        """Describe the Resolution's expectation."""
        return f"Equal to {self.expected}."

    @beat("... hoping it's equal to {expected}.")
    def resolve(self) -> Matcher[Any]:
        """Produce the Matcher to make the assertion."""
        msg = "This resolution raises exception"
        raise ResolutionError(msg)

    def __init__(self, obj: Any) -> None:  # noqa: ANN401
        self.expected = obj


class ResolutionError(Exception): ...
