import cv2
import pickle
import socket
import numpy as np
import argparse
import sys
from datetime import datetime

# Based on https://medium.com/nerd-for-tech/live-streaming-using-opencv-c0ef28a5e497




def main(args):

    # Getting args
    OUTPUT = args.filename


    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()

    ## getting the IP address using socket.gethostbyname() method
    GS_IP = socket.gethostbyname(hostname)

    ## printing the hostname and ip_address
    print(f"Hostname: {hostname}")
    print(f"IP Address: {GS_IP}")
    
    # Non-repeating output if filename not specified
    if (OUTPUT is False):
        # Getting date and time
        now = datetime.now()
        OUTPUT = now.strftime("%d_%m_%Y_%H_%M_%S")

    # Append file type
    OUTPUT = OUTPUT + ".mp4"

    # Stores address of socket and AF_INET specifies ipv4
    # SOCK_DGRAM for UDP
    # Risk of data loss if packet dropped
    # TCP is safer but more complex (Consider updating after proof of concept)
    s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
    s.settimeout(5)

    # Port that we're exposing
    port=6666

    # Binds ip and port into socket
    s.bind((GS_IP,port))

    # Setting vals
    fps = 24
    size = (640,480)
    out = cv2.VideoWriter(OUTPUT, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)


    while True:

        try:
            # Receives data from client and temporarily stores in x
            x = None
            try:
                x=s.recvfrom(1000000)
            except:
                print("Connection timeout.")

            if x is not None:
                # Handling data
                clientip = x[1][0]
                data=x[0]
                data=pickle.loads(data)
                data = cv2.imdecode(data, cv2.IMREAD_COLOR)

                # Display image
                cv2.imshow('received from pi', data)

                out.write(data)

            # breakout key
            if cv2.waitKey(1) & 0xFF == ord('a'):
                break
        except:
            break

    print("Exiting gracefully ...")
    out.release()
    cv2.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description = "Image processing and streaming")
    parser.add_argument('-f', '--filename', default=False, help="(String) Desired name of output file. Do not append file type")
    args = parser.parse_args()
    
    return args

if __name__ == "__main__":
    args = parse_args()
    main(args)
