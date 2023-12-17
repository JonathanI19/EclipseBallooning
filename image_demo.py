import cv2
import numpy as np
from util.camera_processor import CameraProcessor
from util.quad_cell_decoder import QuadCellDecoder
import argparse
import os

DEMO = True

def process_current_frame(qcDec, brightness_vals):

    qcDec.set_intensity_values(brightness_vals)
    qcDec.compute_quadrant_variance()
    qcDec.locate_brightest_quadrants()

def main(args):

    # Get img file
    input_img = args.image

    # Read in image
    img = cv2.imread(input_img)
    
    # We need to set resolutions. 
    # frame_width = int(img.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    # frame_height = int(img.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    frame_height, frame_width, frame_channels = img.shape
    
    print(frame_width)
    print(frame_height) 
    
    # Resolution tuple
    size = (frame_width, frame_height) 

    # Create CameraProcessor object and pass in size of frame
    cProc = CameraProcessor(size)

    # Create a QuadCellDecoder object to process the input frame
    qcDec = QuadCellDecoder()

    cProc.set_frame(img)
    cProc.convert_frame()
    img_hsv = cProc.get_frame()
    cProc.split_frame()
    (q0,q1,q2,q3) = cProc.get_quadrants()
    
    # Getting double of avg brightness for each quadrant
    v0, v1, v2, v3 = cProc.compute_brightness()

    # Process current frame
    process_current_frame(qcDec, (v0, v1, v2, v3))

    # Print out avg brightness values of quadrants
    print(v0, v1, v2, v3)

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
    img_quad = cProc.recombine(q0, q1, q2, q3)

    cv2.imwrite("HSV_"+input_img, img_hsv)
    cv2.imwrite("QUAD_"+input_img, img_quad)
    
def parse_args():
    parser = argparse.ArgumentParser(description = "Image Processing Demonstration")
    parser.add_argument('-i', '--image', required = True, help = "(String) Input image")
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_args()
    main(args)