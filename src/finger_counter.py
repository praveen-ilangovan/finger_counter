# -*- coding: utf-8 -*-

"""
Finger Counter

Counts the raised fingers
"""

# Local imports
from . import cv_utils
from .hand_tracker import HandTracker

def count():
    """
    Turns on the webcam, tracks the hand and counts
    the number of raised fingers
    """

    hand_tracker = HandTracker()

    with cv_utils.LiveFeed() as livefeed:
        while livefeed.isOpened():
            success, img = livefeed.read()
            if not success:
                break

            img_rgb = cv_utils.convert_to_rgb(img)
            results = hand_tracker.hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    fingers = hand_tracker.get_raised_fingers(img, landmarks)
                    print("Fingers: {0}".format(fingers))

            quit_video = livefeed.show(img)
            if quit_video:
                break
