"""
An example of a test module that follows the typical unittest.TestCase test
structure. These tests exercise the Actions to perform drag and drop.
"""

import pytest

from screenpy.actions import See, Eventually
from screenpy.pacing import act, scene
from screenpy.resolutions import ReadsExactly
from screenpy_selenium.actions import Chain, HoldDown, MoveMouse, Open, Release, Wait, Pause
from screenpy_selenium.questions import Text

from ..user_interface.drag_and_drop import (
    FIRST_DRAGGABLE_BOX,
    SECOND_DRAGGABLE_BOX,
    URL,
)


class TestDragAndDrop:
    """
    Shows how to do a drag-and-drop Action.
    """
    @act("Chain")
    @scene("HoldDown")
    @scene("MoveMouse")
    @scene("Release")
    @pytest.mark.xfail
    def test_drag_and_drop(self, marcel) -> None:
        """
        User is able to drag and drop.

        Expected to fail because there is currently an issue in ActionChains.
        """
        marcel.will(Open.their_browser_on(URL))
        marcel.will(Pause(2).second_because("render"))
        marcel.will(Wait.for_the(FIRST_DRAGGABLE_BOX).to_be_clickable())
        marcel.will(Chain(
                MoveMouse.to_the(FIRST_DRAGGABLE_BOX),
                HoldDown.left_mouse_button().on_the(FIRST_DRAGGABLE_BOX),
                MoveMouse.to_the(SECOND_DRAGGABLE_BOX),
                Release.left_mouse_button(),
            ),
        )
        marcel.shall(Eventually(See.the(Text.of_the(FIRST_DRAGGABLE_BOX), ReadsExactly("B"))))
