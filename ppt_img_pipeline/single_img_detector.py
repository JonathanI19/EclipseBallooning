import cv2
import numpy as np
import socket
import pickle
#from picamera2 import Picamera2
import argparse
import sys
from math import sqrt
sys.path.append("../rPi/sun_tracker/util/")
from camera_processor import CameraProcessor
from quad_cell_decoder import QuadCellDecoder
from streaming import StreamingOutput, StreamingHandler, StreamingServer

def process_current_frame(qcDec, brightness_vals):

    qcDec.set_intensity_values(brightness_vals)
    qcDec.compute_quadrant_variance()
    qcDec.locate_brightest_quadrants()
    #qcDec.decode_brightness_into_direction()
    #qcDec.get_stepper_controller().move_steppers()


def main():

    img = cv2.imread("Slide13.jpg", 1)
    h,w,c = img.shape
    # Resolution tuple
    size = (w, h) 

    # Create CameraProcessor object and pass in size of frame
    cProc = CameraProcessor(size)

    # Create a QuadCellDecoder object to process the input frame
    qcDec = QuadCellDecoder(std_dev_coefficient=0.5)

    # reads frames from a camera 
    hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)        

    cv2.imwrite("./hsv_img.jpg", hsv_img)

    
    # Executes brightness evaluation at specified sampling rate
    cProc.set_frame(img)
    cProc.convert_frame()
    cProc.split_frame()
    (q0,q1,q2,q3) = cProc.get_quadrants()
    
    v0, v1, v2, v3 = cProc.compute_brightness()

    # Process current frame
    process_current_frame(qcDec, (v0, v1, v2, v3))

    # Getting results of brightness computation
    q0_is_bright, q1_is_bright, q2_is_bright, q3_is_bright = qcDec.get_brightest_quadrants()
    
    # Converting quadrants based on brightness results
    if q0_is_bright is True:
        q0 = cv2.cvtColor(q0, cv2.COLOR_HSV2RGB)       
    if q1_is_bright is True:
        q1 = cv2.cvtColor(q1, cv2.COLOR_HSV2RGB)
    if q2_is_bright is True:
        q2 = cv2.cvtColor(q2, cv2.COLOR_HSV2RGB)
    if q3_is_bright is True:
        q3 = cv2.cvtColor(q3, cv2.COLOR_HSV2RGB)
    
    # Example of recombining frame
    new_frame = cProc.recombine(q0, q1, q2, q3)

    cv2.imwrite("result2.jpg", new_frame)
    print(f"{v0}  {v1}  {v2}  {v3}")

    
if __name__ == "__main__":
    main()
