import cv2
import numpy as np

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
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #out = cv2.VideoWriter('output.mp4', fourcc, 20.0, size)
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 24, size)

    # loop runs if capturing has been initialized. 
    while(True):
        # reads frames from a camera 
        # ret checks return at each frame
        ret, frame = cap.read() 
        if (ret == True):
            # Converts to grayscale space, OCV reads colors as BGR
            # frame is converted to gray
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # output the frame
            out.write(frame) 
            
            # The original input frame is shown in the window 
            cv2.imshow('Original', frame)
        
            # The window showing the operated video stream 
            cv2.imshow('frame', gray)
        
            
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