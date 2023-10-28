# Module Overview

## Main

**Write up required**

## Utils

**Write up required**

## SSH

SSH based on code found at https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/

1. Get IP Address of rPi
	```ifconfig```

	* Home IP: 192.168.1.68
	* School IP: 

2. Run Script with video streaming enabled

	```python main.py -ssh=True```
	
3. Connect to video streaming web server (**Note: Must be connected to same network**)

	```http://<rPi_IP_Address>:8000```
