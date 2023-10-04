import cv2
import numpy as np
from util.camera_processor import Camera_Processor

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
    
    size = (frame_width, frame_height) 
    
    fps = 24
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    frame_count = 0
    samples_per_second = 1
    cProc = Camera_Processor(size)

    # loop runs if capturing has been initialized. 
    while(True):
        # reads frames from a camera 
        # ret checks return at each frame
        ret, frame = cap.read() 
        if (ret == True):
            frame_count+=1
            # output the frame
            out.write(frame) 
            
            # The original input frame is shown in the window 
            cv2.imshow('Original', frame)
            if(frame_count == (fps/samples_per_second)):
                frame_count = 0
                cProc.set_frame(frame)
                cProc.convert_frame()
                (q0,q1,q2,q3) = cProc.split_frame()
                cv2.imshow('q0', q0)
                cv2.imshow('q1', q1)
                cv2.imshow('q2', q2)
                cv2.imshow('q3', q3)
                
                # Getting brightness values
                v0, v1, v2, v3 = cProc.get_brightness()

                # converting to list and getting index of brightest
                values = [v0,v1,v2,v3]
                quadrants = [q0,q1,q2,q3]
                brightest = np.argmax(values)

                # Converting brightest back to original color space
                quadrants[brightest] = cv2.cvtColor(quadrants[brightest], cv2.COLOR_HSV2RGB)

                
                # Example of recombining frame
                half_w = frame_width//2
                half_h = frame_height//2
                new_frame = frame
                new_frame[:half_h, half_w:] = quadrants[0]
                new_frame[:half_h, :half_w] = quadrants[1]
                new_frame[half_h:, :half_w] = quadrants[2]
                new_frame[half_h:, half_w:] = quadrants[3]
                cv2.imshow("New Frame", new_frame)

        
            # Wait for 'a' key to stop the program 
            if cv2.waitKey(1) & 0xFF == ord('a'):
                break

        else:
            break

    # Close the window / Release webcam
    cap.release()
    
    # After we release our webcam, we also release the out-out.release() 
    
    # De-allocate any associated memory usage 
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()