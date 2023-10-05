import cv2
from statistics import mean
import numpy as np

class Camera_Processor:
    """Contains processing information to analyze quadrants of an image.
    """ 

    def __init__(self, size):
        """Constructor

        Args:
            size (tuple of ints): (width, height) of image
        """        

        self.__frame = []
        self.__q0 = []
        self.__q1 = []
        self.__q2 = []
        self.__q3 = []
        self.w, self.h = size

        # Half of the w/h of frame rounded down
        self.half_w = self.w//2
        self.half_h = self.h//2

        # Pixel density
        self.pxl = self.half_w*self.half_h

    def set_frame(self, frame):
        """Sets new frame for processing

        Args:
            frame (list of ints): new cv2 frame to be processed
        """        
        self.__frame = frame

    def convert_frame(self):
        """Converts frame to HSV color scheme
        """        
        self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_RGB2HSV)

    def split_frame(self):
        """Splits frame into four separate quadrants

        Returns:
            Tuple: matrices for each quadrant for display
        """
        #              |
        #        [1]   |   [0]
        #              |
        #      -----------------
        #              |
        #        [2]   |   [3]
        #              |
               
        self.__q0 = self.__frame[:self.half_h, self.half_w:]
        self.__q1 = self.__frame[:self.half_h, :self.half_w]
        self.__q2 = self.__frame[self.half_h:, :self.half_w]
        self.__q3 = self.__frame[self.half_h:, self.half_w:]
        return(self.__q0, self.__q1, self.__q2, self.__q3)


    def get_brightness(self):
        """Calculates avg value of each quadrant

        Returns:
            Tuple of Doubles: Avg value of each quadrant
        """        
        v0 = np.sum(self.__q0[:,:,2])
        avg_v0 = v0 / self.pxl

        v1 = np.sum(self.__q1[:,:,2])
        avg_v1 = v1 / self.pxl

        v2 = np.sum(self.__q2[:,:,2])
        avg_v2 = v2 / self.pxl

        v3 = np.sum(self.__q3[:,:,2])
        avg_v3 = v3 / self.pxl

        return(avg_v0, avg_v1, avg_v2, avg_v3)
    
    def recombine(self, quadrants):
        """Recombines split quadrants into a single frame

        Args:
            quadrants (list): List of quadrant data

        Returns:
            List: New frame to be displayed
        """        
        new_frame = self.__frame
        new_frame[:self.half_h, self.half_w:] = quadrants[0]
        new_frame[:self.half_h, :self.half_w] = quadrants[1]
        new_frame[self.half_h:, :self.half_w] = quadrants[2]
        new_frame[self.half_h:, self.half_w:] = quadrants[3]
        return new_frame
