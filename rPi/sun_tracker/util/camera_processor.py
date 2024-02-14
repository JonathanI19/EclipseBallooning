import cv2
from statistics import mean
import numpy as np

class CameraProcessor:
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
        self.__width, self.__height = size

        # Half of the w/h of frame rounded down
        self.__half_width = self.__width//2
        self.__half_height = self.__height//2

        # Pixel density
        self.self.__pxl = self.__half_width*self.__half_height

        # Initialize frame to none
        self.__frame = None

    def set_frame(self, frame):
        """Sets new frame for processing

        Args:
            frame (list of ints): new cv2 frame to be processed
        """        
        self.__frame = frame

    def get_frame(self):
        """gets __frame member variable

        Returns:
            List: Frame data
        """        
        return self.__frame

    def convert_frame(self):
        """Converts frame to HSV color scheme
        """        
        self.set_frame(cv2.cvtColor(self.__frame, cv2.COLOR_RGB2HSV))

    def set_quadrants(self, q0, q1, q2, q3):
        """Sets quadrant data

        Args:
            q0 (list): q0 frame data
            q1 (list): q1 frame data
            q2 (list): q2 frame data
            q3 (list): q3 frame data
        """
        self.__q0 = q0
        self.__q1 = q1
        self.__q2 = q2
        self.__q3 = q3

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
               
        self.set_quadrants(self.__frame[:self.__half_height, self.__half_width:], self.__frame[:self.__half_height, :self.__half_width], self.__frame[self.__half_height:, :self.__half_width], self.__frame[self.__half_height:, self.__half_width:])
    
    def get_quadrants(self):
        """gets __q0, __q1, __q2, __q3 member variables

        Returns:
            Tuple: Quadrants
        """         
    
        return(self.__q0, self.__q1, self.__q2, self.__q3)


    def compute_brightness(self):
        """Calculates avg value of each quadrant

        Returns:
            Tuple of Doubles: Avg value of each quadrant
        """        

        q0, q1, q2, q3 = self.get_quadrants()

        v0 = np.sum(q0[:,:,2])
        avg_v0 = v0 / self.self.__pxl

        v1 = np.sum(q1[:,:,2])
        avg_v1 = v1 / self.self.__pxl

        v2 = np.sum(q2[:,:,2])
        avg_v2 = v2 / self.self.__pxl

        v3 = np.sum(q3[:,:,2])
        avg_v3 = v3 / self.self.__pxl

        return(avg_v0, avg_v1, avg_v2, avg_v3)
    
    def recombine(self, q0, q1, q2, q3):
        """FOR DEMO ONLY - Recombines split quadrants into a single frame

        Args:
            q0: Quadrant 0 frame data
            q1: Quadrant 1 frame data
            q2: Quadrant 2 frame data  
            q3: Quadrant 3 frame data

        Returns:
            List: New frame to be displayed
        """        
        new_frame = self.get_frame()
        new_frame[:self.__half_height, self.__half_width:] = q0
        new_frame[:self.__half_height, :self.__half_width] = q1
        new_frame[self.__half_height:, :self.__half_width] = q2
        new_frame[self.__half_height:, self.__half_width:] = q3
        return new_frame
