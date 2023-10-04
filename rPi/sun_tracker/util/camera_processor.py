import cv2

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

    def set_frame(self, frame):
        self.__frame = frame

    def convert_frame(self):
        self.__frame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2HSV)

    def split_frame(self):
        self.__q0 = self.__frame[:self.half_h, self.half_w:]
        self.__q1 = self.__frame[:self.half_h, :self.half_w]
        self.__q2 = self.__frame[self.half_h:, :self.half_w]
        self.__q3 = self.__frame[self.half_h:, self.half_w:]
        return(self.__q0, self.__q1, self.__q2, self.__q3)


    #def get_brightness(self):
        
