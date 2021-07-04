# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Uses mediapipe module to track hands
"""

# Project specific imports
import cv2 as cv
import mediapipe as mp #type: ignore
from typing import List

#-----------------------------------------------------------------------------#
#
# MediaPipe HandTracker
#
#-----------------------------------------------------------------------------#
class HandTracker():

    INDEX_FINGER = (5, 8, "index")
    MIDDLE_FINGER = (9, 12, "middle")
    RING_FINGER = (13, 16, "ring")
    PINKY_FINGER = (17, 20, "pinky")
    FINGERS = (INDEX_FINGER,MIDDLE_FINGER, RING_FINGER, PINKY_FINGER)

    def __init__(self, max_hands: int=1):
        super().__init__()
        self.__mp_hands = mp.solutions.hands
        self.__mp_draw = mp.solutions.drawing_utils

        self.__hands = self.__mp_hands.Hands(max_num_hands=max_hands,
                                             min_detection_confidence=0.6)

    #--------------------------------------------------------------------------#
    # Properties
    #--------------------------------------------------------------------------#
    @property
    def hands(self):
        return self.__hands

    #--------------------------------------------------------------------------#
    # Methods
    #--------------------------------------------------------------------------#
    def get_raised_fingers(self, img, landmarks) -> List:
        """
        Find the raised fingers and return a list

        rtype:
            List

        Returns:
            A list of fingers that are raised.
        """
        raised_fingers = []
        h,w,c = img.shape

        for finger in HandTracker.FINGERS:
            if len(landmarks.landmark) < finger[1]:
                continue

            base = landmarks.landmark[finger[0]]
            tip = landmarks.landmark[finger[1]]

            # print(landmarks.landmark[finger[0]])
            # print(landmarks.landmark[finger[1]])

            # Base: red
            bx, by = (int(base.x*w), int(base.y*h))
            # Draw a circle around the tip
            cv.circle(img, (bx,by), 10, (0,0,125), cv.FILLED)

            # Tip: green
            tx, ty = (int(tip.x*w), int(tip.y*h))
            # Draw a circle around the tip
            cv.circle(img, (tx,ty), 10, (0,125,0), cv.FILLED)

            if landmarks.landmark[finger[1]].y < landmarks.landmark[finger[0]].y:
                raised_fingers.append(finger[2])

        return raised_fingers