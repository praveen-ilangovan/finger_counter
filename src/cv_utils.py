# -*- coding: utf-8 -*-

"""
Gesture Volume Control

Module that has all the opencv functionalities used in this
project.
"""

# Builtins
from __future__ import annotations

# Project specific imports
import cv2 as cv #type: ignore
import numpy as np
from typing import Union, Optional, List

# Local imports
from .hand_tracker import HandTracker

HAND_TRACKER = HandTracker()

#-----------------------------------------------------------------------------#
#
# Cv VideoCapture as Context Manager
#
#-----------------------------------------------------------------------------#
class VideoCapture(cv.VideoCapture):
    def __init__(self, filepath_or_index: Union[str,int],
                       apipref: Optional[int]=None,
                       waittime: int=20,
                       quitkey: str="q"):
        """ Extends cv.VideoCapture to be used as context manager.

        Args:
            filepath_or_index str|int: Filepath/Index
            apipref int|None: Prefered Capture API backends
            waittime int: Wait time to show the image
            quitkey str: Keyboard character to press to quit capturing

        rtype:
            VideoCapture

        Returns:
            An instance of VideoCapture
        """
        super().__init__(filepath_or_index, apipref)
        self.__waittime = waittime
        self.__quitkey = ord(quitkey)

    #-------------------------------------------------------------------------#
    # Context managers
    #-------------------------------------------------------------------------#
    def __enter__(self) -> VideoCapture:
        self.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        self.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.release()
        cv.destroyAllWindows()

    #-------------------------------------------------------------------------#
    # Extra methods
    #-------------------------------------------------------------------------#
    def show(self, img: np.ndarray, winname: str="Volume Controller") -> bool:
        """
        Show the image in a window and listen to the keyboard events to stop
        showing.

        Args:
            img np.ndarray: Image in numpy array format
            winname str: Optionally name the window

        rtype:
            bool

        Returns:
            Returns True if quit key is pressed
        """
        # Display the video
        cv.imshow(winname, img)

        # Keep track of the keyboard events. Listen for q key press
        key = cv.waitKey(self.__waittime) & 0xFF
        return key == self.__quitkey
    
#-----------------------------------------------------------------------------#
# LiveFeed from webcam
#-----------------------------------------------------------------------------#
class LiveFeed(VideoCapture):
    def __init__(self, webcam: int=0):
        super().__init__(webcam, cv.CAP_DSHOW)

#-----------------------------------------------------------------------------#
#
# Image processing
#
#-----------------------------------------------------------------------------#
def convert_to_rgb(img: np.ndarray) -> np.ndarray:
    """ Convert the image's colour space to rgb

    Args:
        img numpy.ndarray: Image in an numpy array format

    rtype:
        numpy.ndarray

    Returns:
        A numpy array
    """
    return cv.cvtColor(img, cv.COLOR_BGR2RGB)

def get_fingers(img: np.ndarray) -> List:
    """
    Get the raised fingers

    Args:
        img numpy.ndarray: Image in an numpy array format

    rtype:
        List

    Returns:
        A list of Fingers
    """
    img_rgb = convert_to_rgb(img)
    return HAND_TRACKER.get_raised_fingers(img, img_rgb)

def display_fingers(img: np.ndarray) -> None:
    """
    Find the fingers and display the information like
    their landmarks, number of fingers, their names, etc

    Args:
        img numpy.ndarray: Image in an numpy array format
    """
    fingers = get_fingers(img)
    if not fingers:
        return None

    txt = "Fingers: {0}".format(", ".join(fingers))
    cv.putText(img, txt, (10,img.shape[0]-50), cv.FONT_HERSHEY_PLAIN, 1, (0,120,0), 2)