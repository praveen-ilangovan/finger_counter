# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Uses mediapipe module to track hands
"""

# Project specific imports
import numpy as np
import mediapipe as mp #type: ignore
from typing import List, Tuple

#-----------------------------------------------------------------------------#
#
# Finger
#
#-----------------------------------------------------------------------------#
class Finger():
    def __init__(self, name: str, indices: Tuple, is_thumb: bool=False) -> None:
        """
        Indices is the list of four landmarks on each finger
        """
        super().__init__()
        self.__name = name
        self.__base, self.__pip, self.__dip, self.__tip = indices
        self.__is_thumb = is_thumb

    #--------------------------------------------------------------------------#
    # Properties
    #--------------------------------------------------------------------------#
    @property
    def name(self):
        return self.__name

    @property
    def is_thumb(self):
        return self.__is_thumb

    #--------------------------------------------------------------------------#
    # Methods
    #--------------------------------------------------------------------------#
    def is_raised(self, landmarks) -> bool:
        """
        Check if the finger is raised using the landmarks.

        # indices: 

        Checks:
            If the tip's y is lower than base'y
            If so, check if the intermediate indices are lower too..

        rtype:
            bool
        """

        def get_x(index: int)-> float:
            return landmarks.landmark[index].x

        def get_y(index: int)-> float:
            return landmarks.landmark[index].y

        if len(landmarks.landmark) < self.__tip:
            return False

        base_y = get_y(self.__base)
        tip_y = get_y(self.__tip)

        if tip_y < base_y:
            # Tip is lower than base, check each index to make sure, the finger
            # is really upright
            ys = (base_y, get_y(self.__pip), get_y(self.__dip), tip_y)
            for i in range(len(ys)-1):
                if ys[i+1] >= ys[i]:
                    return False

            if self.__is_thumb:
                # Work out the direction of the hand, using the
                # x positions of index and middle finger and then figure
                # out if the thumb is extended out of the index finger
                # to count it

                index_x = get_x(8)
                middle_x = get_x(12)
                tip_x = get_x(self.__tip)

                if index_x < middle_x:
                    if tip_x >= index_x:
                        return False
                else:
                    if tip_x <= index_x:
                        return False

            return True
        
        return False

#-----------------------------------------------------------------------------#
#
# MediaPipe HandTracker
#
#-----------------------------------------------------------------------------#
class HandTracker():
    def __init__(self, max_hands: int=1) -> None:
        super().__init__()
        self.__mp_hands = mp.solutions.hands
        self.__mp_draw = mp.solutions.drawing_utils

        self.__hands = self.__mp_hands.Hands(max_num_hands=max_hands,
                                             min_detection_confidence=0.6)

        self.__fingers = (Finger("Thumb", (1,2,3,4), True),
                          Finger("Index", (5,6,7,8)),
                          Finger("Middle", (9,10,11,12)),
                          Finger("Ring", (13,14,15,16)),
                          Finger("Pinky", (17,18,19,20)))

    #--------------------------------------------------------------------------#
    # Methods
    #--------------------------------------------------------------------------#
    def get_raised_fingers(self, img:np.ndarray, img_rgb) -> List:
        """
        Find the raised fingers and return a list

        rtype:
            List

        Returns:
            A list of fingers that are raised.
        """
        results = self.__hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                return [f.name for f in self.__fingers if f.is_raised(landmarks)]

        return []

