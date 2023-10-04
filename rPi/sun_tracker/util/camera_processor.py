import cv2
from statistics import mean
import numpy as np

class Camera_Processor:
    def __init__(self, size):
        self.__frame = []
        self.__q0 = []
        self.__q1 = []
        self.__q2 = []
        self.__q3 = []
        self.w, self.h = size
        self.half_w = self.w//2
        self.half_h = self.h//2
        self.pxl = self.half_w*self.half_h

    def set_frame(self, frame):
        self.__frame = frame

    def convert_frame(self):
        self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_RGB2HSV)

    def split_frame(self):
        self.__q0 = self.__frame[:self.half_h, self.half_w:]
        self.__q1 = self.__frame[:self.half_h, :self.half_w]
        self.__q2 = self.__frame[self.half_h:, :self.half_w]
        self.__q3 = self.__frame[self.half_h:, self.half_w:]
        return(self.__q0, self.__q1, self.__q2, self.__q3)


    def get_brightness(self):
        v0 = np.sum(self.__q0[:,:,2])
        avg_v0 = v0 / self.pxl

        v1 = np.sum(self.__q1[:,:,2])
        avg_v1 = v1 / self.pxl

        v2 = np.sum(self.__q2[:,:,2])
        avg_v2 = v2 / self.pxl

        v3 = np.sum(self.__q3[:,:,2])
        avg_v3 = v3 / self.pxl

        return(avg_v0, avg_v1, avg_v2, avg_v3)
