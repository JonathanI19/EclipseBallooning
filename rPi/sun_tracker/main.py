import cv2
import numpy as np
from util.camera_processor import CameraProcessor
from util.quad_cell_decoder import QuadCellDecoder
from picamera2 import Picamera2

DEMO = True

def process_current_frame(qcDec, brightness_vals):

    qcDec.set_intensity_values(brightness_vals)
    qcDec.compute_quadrant_variance()
    qcDec.locate_brightest_quadrants()
    qcDec.decode_brightness_into_direction()
    qcDec.get_servo_controller().move_servos()

def main():

    if DEMO is True:
        # Start window thread
        cv2. startWindowThread()
    
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
        
        # The original input frame is shown in the window 
        cv2.imshow('Original', frame)
        
        # Executes brightness evaluation at specified sampling rate
        if(frame_count == (fps//samples_per_second)):
            frame_count = 0
            cProc.set_frame(frame)
            cProc.convert_frame()
            cProc.split_frame()
            (q0,q1,q2,q3) = cProc.get_quadrants()

            # Display Quadrant HSV if DEMO is True
            if DEMO is True:
                cv2.imshow('q0', q0)
                cv2.imshow('q1', q1)
                cv2.imshow('q2', q2)
                cv2.imshow('q3', q3)
        
            # Getting double of avg brightness for each quadrant
            v0, v1, v2, v3 = cProc.compute_brightness()

            # Process current frame
            process_current_frame(qcDec, (v0, v1, v2, v3))

            # Print out avg brightness values of quadrants if DEMO is True
            # print(v0, v1, v2, v3)

            # Showcases brightest quadrant(s) if DEMO is True
            if DEMO is True:

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
            break
    
    # After we release our webcam, we also release the out
    out.release()

    # De-allocate any associated memory usage 
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()