import cv2
import numpy as np
import socket
import pickle
from util.camera_processor import CameraProcessor
from util.quad_cell_decoder import QuadCellDecoder
from util.streaming import StreamingOutput, StreamingHandler, StreamingServer
from picamera2 import Picamera2
import argparse
import sys


def process_current_frame(qcDec, brightness_vals):

    qcDec.set_intensity_values(brightness_vals)
    qcDec.compute_quadrant_variance()
    qcDec.locate_brightest_quadrants()
    qcDec.decode_brightness_into_direction()
    qcDec.get_stepper_controller().move_steppers()

def socket_init(ip):

    # Set socket data as ipv4 and udp
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)

    # Specify ip and port
    server_ip = ip
    server_port = 6666
    return s, server_ip, server_port

def main(args):
    
    DISPLAY = bool(args.display)
    STREAM = bool(args.stream)
    QUAD = bool(args.quad)
    GS_IP = args.ip
    
    if DISPLAY is True:
        # Start window thread
        cv2.startWindowThread()
    
    # Create picam2 object and start collecting data
    picam2 = Picamera2()
    # picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    picam2.start()
    
    # Get first frame
    frame = picam2.capture_array()
    frame_height, frame_width, depth = frame.shape
    
    # Resolution tuple
    size = (frame_width, frame_height) 
    
    # Set fps value and create videoWriter object "out"
    fps = 24
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    if STREAM is True:
        if (GS_IP == 0):
            print("No IP Set")
            sys.exit()
        s, server_ip, server_port = socket_init(ip = GS_IP)

    # Variables for sampling
    frame_count = 0
    samples_per_second = 24

    # Create CameraProcessor object and pass in size of frame
    cProc = CameraProcessor(size)

    # Create a QuadCellDecoder object to process the input frame
    qcDec = QuadCellDecoder()

    # loop runs if capturing has been initialized. 
    while(True):

        # reads frames from a camera 
        frame =picam2.capture_array() 
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)        

        # Keep track of frame_count for sampling
        frame_count+=1

        # output the frame
        out.write(frame) 
        
        if DISPLAY is True:
            # The original input frame is shown in the window 
            cv2.imshow('Original', frame)

        # Execute if streaming flag set
        if STREAM is True:
            ret,buffer = cv2.imencode(".jpg",frame,[int(cv2.IMWRITE_JPEG_QUALITY),30])
            x_as_bytes = pickle.dumps(buffer)
            s.sendto((x_as_bytes),(server_ip,server_port))
        
        # Executes brightness evaluation at specified sampling rate
        if(frame_count == (fps//samples_per_second)):
            frame_count = 0
            cProc.set_frame(frame)
            cProc.convert_frame()
            cProc.split_frame()
            (q0,q1,q2,q3) = cProc.get_quadrants()

            # Display Quadrant HSV if QUAD is True
            if QUAD is True:
                cv2.imshow('q0', q0)
                cv2.imshow('q1', q1)
                cv2.imshow('q2', q2)
                cv2.imshow('q3', q3)
        
            # Getting double of avg brightness for each quadrant
            v0, v1, v2, v3 = cProc.compute_brightness()

            # Process current frame
            process_current_frame(qcDec, (v0, v1, v2, v3))

            # Showcases brightest quadrant(s) if QUAD is True
            if QUAD is True:

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

                cv2.imshow("New Frame", new_frame)

    
        # Wait for 'a' key to stop the program 
        if cv2.waitKey(1) & 0xFF == ord('a'):
            #qcDec.get_stepper_controller().cleanup()
            break
    
    # After we release our webcam, we also release the out
    out.release()

    # De-allocate any associated memory usage 
    cv2.destroyAllWindows()
    
    
def parse_args():
    parser = argparse.ArgumentParser(description = "Image processing and streaming")
    
    # Add arguments
    parser.add_argument('-q', '--quad', default=False, help="(Boolean) Toggles Quadrant Demo Functionality")
    parser.add_argument('-s', '--stream', default=False, help="(Boolean) Toggles web streaming")
    parser.add_argument('-d', '--display', default=False, help="(Boolean) Toggles local input frame display")
    parser.add_argument('-i', '--ip', default=0, help="(String) Set ip of ground station")
    args = parser.parse_args()
    
    return args

     
if __name__ == "__main__":
    args = parse_args()
    main(args)
