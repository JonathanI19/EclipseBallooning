import cv2
import numpy as np
from util.camera_processor import CameraProcessor
from util.quad_cell_decoder import QuadCellDecoder

DEMO = True

def switch_case(input):
    switcher = {
        (True, False, False, False): "Pan Right",
        (False, False, False, True): "Pan Right", 
        (False, False, True, False): "Pan Left", 
        (False, True, False, False): "Pan Left", 
        (True, False, False, True): "Pan Right", 
        (False, True, True, False): "Pan Left"
    }
    return switcher.get(input, "Freeze")

def main():

    # This will return video from the first webcam on your computer.
    cap = cv2.VideoCapture(0)  
    
    # We need to check if camera 
    # is opened previously or not 
    if (cap.isOpened() == False):  
        print("Error reading video file") 

    # We need to set resolutions. 
    # so, convert them from float to integer. 
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
    
    # Resolution tuple
    size = (frame_width, frame_height) 
    
    # Set fps value and create videoWriter object "out"
    fps = 24
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # Variables for sampling
    frame_count = 0
    samples_per_second = 24

    # Create Camera_Processor object and pass in size of frame
    cProc = CameraProcessor(size)
    qcDec = QuadCellDecoder()

    # loop runs if capturing has been initialized. 
    while(True):

        # reads frames from a camera 
        # ret checks return at each frame
        ret, frame = cap.read() 


        if (ret == True):

            # Keep track of frame_count for sampling
            frame_count+=1

            # output the frame
            out.write(frame) 
            

            # The original input frame is shown in the window 
            # cv2.imshow('Original', frame)
            
            # Executes brightness evaluation at specified sampling rate
            if(frame_count == (fps//samples_per_second)):
                frame_count = 0
                cProc.set_frame(frame)
                cProc.convert_frame()
                cProc.split_frame()
                (q0,q1,q2,q3) = cProc.get_quadrants()
            
                # Getting double of avg brightness for each quadrant
                v0, v1, v2, v3 = cProc.compute_brightness()

                qcDec.set_intensity_values((v0,v1,v2,v3))
                qcDec.compute_quadrant_variance()
                qcDec.locate_brightest_quadrants()

                # Showcases brightest quadrant if DEMO is True
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
                    
                    switch_output = switch_case((q0_is_bright, q1_is_bright, q2_is_bright, q3_is_bright))
                    print(switch_output)

                    # Example of recombining frame
                    new_frame = cProc.recombine(q0, q1, q2, q3)

                    new_frame = cv2.resize(new_frame, (1920,1080))
                    cv2.imshow("Processed Frame", new_frame)

        
            # Wait for 'a' key to stop the program 
            if cv2.waitKey(1) & 0xFF == ord('a'):
                break

        else:
            break

    # Close the window / Release webcam
    cap.release()
    
    # After we release our webcam, we also release the out
    out.release()

    # De-allocate any associated memory usage 
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()