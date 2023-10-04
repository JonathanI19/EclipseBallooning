import cv2

class Camera_Processor:
    def __init__(self, frame):
        self.__frame=frame
        self.__q0 = []
        self.__q1 = []
        self.__q2 = []
        self.__q3 = []

    def split_frame(self):
        h,w,channels = 