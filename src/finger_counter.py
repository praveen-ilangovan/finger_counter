# -*- coding: utf-8 -*-

"""
Finger Counter

Counts the raised fingers
"""

# Local imports
from . import cv_utils

def count():
    """
    Turns on the webcam, tracks the hand and counts
    the number of raised fingers
    """
    with cv_utils.LiveFeed() as livefeed:
        while livefeed.isOpened():
            success, img = livefeed.read()
            if not success:
                break

            cv_utils.display_fingers(img)

            quit_video = livefeed.show(img)
            if quit_video:
                break
