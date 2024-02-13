from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy import Either

from screenpy_examples.screenpy.silently_logging.actions import (
    PerformFail,
    PerformFirst,
    PerformSecond,
)

if TYPE_CHECKING:
    from screenpy import Actor


def test_first_action_pass(marcel: Actor) -> None:
    """
    Demonstrates logging of a `Either`:
        perform first action which passes
        and not perform the second action

    Marcel tries to PerformFirst
        Marcel tries to PerformPass
            Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(Either(PerformFirst()).otherwise(PerformSecond()))


def test_first_action_fail(marcel: Actor) -> None:
    """
    Demonstrates logging of a `Either`:
        perform first action which fails
        and then perform second action which passes

    Marcel tries to PerformSecond
        Marcel tries to PerformPass
            Marcel sees if simpleQuestion is equal to True.
    """
    marcel.will(Either(PerformFirst(PerformFail())).otherwise(PerformSecond()))


def test_first_and_second_action_fail(marcel: Actor) -> None:
    """
    Demonstrates logging of a `Either`:
        perform the first action which fails
        and perform second action which fails

    Marcel tries to PerformSecond
        Marcel tries to PerformFail
            Marcel sees if simpleQuestion is equal to False.
                Marcel examines SimpleQuestion
                    => True
                ... hoping it's equal to False.
                    => <False>
                ***ERROR***

    AssertionError:
    Expected: <False>
         but: was <True>
    """
    marcel.will(
        Either(PerformFirst(PerformFail())).otherwise(PerformSecond(PerformFail()))
    )