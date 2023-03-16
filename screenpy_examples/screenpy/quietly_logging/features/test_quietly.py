import pytest

from screenpy import Actor
from screenpy.actions import Eventually

from screenpy_examples.screenpy.quietly_logging.actions import (
    DoA,
    DoB,
    DoChatty,
    DoChattyFail,
    DoFail,
    DoFailCounter,
    DoPass,
    DoPassAfterAWhile,
    Quietly,
)


def test_eventually_succeeds(marcel: Actor) -> None:
    marcel.will(Eventually(DoPassAfterAWhile()).for_(1).seconds())


def test_eventually_fails(marcel: Actor) -> None:
    marcel.will(Eventually(DoFailCounter()).for_(1).seconds())


def test_passes_without_quietly(marcel: Actor) -> None:
    """
    Generates a normal log:

    Marcel tries to DoChatty
        Marcel tries to DoA
            Marcel tries to DoB
                Marcel tries to DoPass
                    Marcel sees if simple question is equal to True.
                        ... hoping it's equal to True
                            => True
    Marcel tries to DoB
        Marcel tries to DoPass
            Marcel sees if simple question is equal to True.
                ... hoping it's equal to True
                    => True
    """
    marcel.will(DoChatty(DoA(DoB(DoPass()))))
    marcel.will(DoB(DoPass()))


def test_passes_with_quietly(marcel: Actor) -> None:
    """
    Generates a quiet log:

    Marcel tries to DoChatty
    Marcel tries to DoB
    """
    marcel.will(DoChatty(Quietly(DoA(DoB(DoPass())))))
    marcel.will(DoB(Quietly(DoPass())))


def test_fails_without_quietly(marcel) -> None:
    """
    Generates a normal log showing failure:

    Marcel tries to DoChattyFail
        Marcel tries to DoA
            Marcel tries to DoB
                Marcel tries to DoFail
                    Marcel sees if simple question is equal to False.
                        ... hoping it's equal to False
                            => False
                        ***ERROR***

    AssertionError:
    Expected: <False>
         but: was <True>
    """
    marcel.will(DoChattyFail(DoA(DoB(DoFail()))))
    marcel.will(DoB(DoPass()))


def test_fails_with_quietly(marcel) -> None:
    """
    Generates a "quiet" log, but demonstrates that in a case of failure the output
    looks identical to a normal log.

    Marcel tries to DoChattyFail
        Marcel tries to DoA
            Marcel tries to DoB
                Marcel tries to DoFail
                    Marcel sees if simple question is equal to False.
                        ... hoping it's equal to False
                            => False
                        ***ERROR***

    AssertionError:
    Expected: <False>
         but: was <True>
    """
    marcel.will(DoChattyFail(Quietly(DoA(DoB(DoFail())))))
    marcel.will(DoB(Quietly(DoPass())))