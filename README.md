# Team 02 NASA Solar Eclipse Ballooning
This repository contains a Python implementation of the solar tracking algorithms designed by the NASA Solar Eclipse Ballooning Team as part their [Senior Design](https://engineering.temple.edu/students/senior-design) capstone project at Temple University. The software also performs real-time video capture and livestreaming via UDP.

# Solar Tracking Methodology
The goal of the 2024 NASA Solar Eclipse Ballooning project is to record, store, and distribute video footage of the total solar eclipse visible from the continental United States on April 8, 2024. The team realizes this objective by designing a high-altitude ballooning payload capable of capturing and streaming the eclipse from stratospheric altitudes. To combat unwanted rotation of the payload due to wind forces during the flight, the team utilizes a rotating platform to continuously adjust the position of the camera systems ensuring that they are always oriented in the direction of the sun. The software contained in this repository is responsible for controlling the rotation of the camera platform based upon the position of the sun in the sky. The solar location and platform control functionality are implemented in Python and meant for use with a Raspberry Pi computing platform.

The Pi expects two inputs to make decisions about the location of the sun in the sky relative to the orientation of the onboard cameras. The first input is from a photodiode-based solar sensor circuit designed by the team. The circuit consists of four identical transimpedance amplification channels that receive photocurrent input from strategically placed photodiodes. The circuit outputs four analog voltage signals based upon which diode is currently "seeing" the most light. One of the diodes is aligned with the cameras on the payload (i.e., the "camera diode"). If this diode is **not** producing the strongest photocurrent (i.e., another diode is probably facing the sun), algorithmic control decides to rotate the platform either left or right depending upon the status of the other diodes. It should be noted that the four analog voltage signals are first sampled by an Arduino ADC before they are fed into the algorithms running on the Pi. The `SolarSensorDecoder` module handles all decoding, processing, and decision making for information from the solar sensor.

The second input comes from a [Pi camera](https://www.amazon.com/Smraza-Raspberry-Megapixels-Adjustable-Fish-Eye/dp/B07L2SY756/ref=sr_1_5?crid=OFUB37MKOJQ3&dib=eyJ2IjoiMSJ9.3F1QsqAsv--X_vzV3o5VcYBG_dNu1GUIAzLwIGR8jKH5Iup20iYo3WLOPRLTSwAG14FQU9qTXv_MnUlCEsptsIP3nmxbRlfGd-6cfSXiBOwJNIQt38TfP6rv3R8nJYaxkxyNozzXjFJuacu70vqzJLoLFKmZZggoeTQUBQPqwMrG964ZnrAaHWs_PyPR0B8eJJrqczH_pSn1WBWevDvSujRWEe3rWS1nVbF42HjaHmCa_UC3G3BE11ydo86Fqzb8Bv0OwCHDIC2iqDWFRA0R4ELczjAJWykv8DUZmlpxLE8.UZmfeY8FGNlmjTk5hFqK3WB3Pdw8MuLfosmOQsPGE5Y&dib_tag=se&keywords=wide-angle+lens+pi+camera&qid=1714136104&s=electronics&sprefix=wide-angle+lens+pi+camera%2Celectronics%2C65&sr=1-5). The input image is split into four quadrants in what the team deems a quad-cell-based image processing approach. The quadrants are converted to HSV (hue-saturation-value) color space to extract information about the relative distribution of brightness/intensity across the frame. The average intensity of each quadrant is calculated using the "value" parameter. The `QuadCellDecoder` then makes platform rotation decisions based upon these four intensity values. All pre-processing of the image is performed in the `CameraProcessor` module. The image processing algorithm (i.e., "camera control") is only performed when the "camera diode" is aligned with the sun as determined by the `SolarSensorDecoder` instance. Thus, the solar sensor algorithm performs general location of the sun (for instance, the sun could be located behind the camera and out of its field of view, in which case camera tracking would be inaccurate), while image processing is used for more granular control and centering of the sun in frame. The figure below shows the entire flow of the solar tracking methods implemented in this project.

![image](https://github.com/JonathanI19/EclipseBallooning/assets/98061409/a5cd06f8-e37f-4464-8744-5f96992db36d)

# Platform Rotation
The `StepperController` module uses a two-bit interface to send movement commands to an Arduino (or similar embedded system). The two-bit interface is implemented via the GPIO pins on the Pi. The Arduino driver is instructed to rotate the platform left or right depending on the current position of the sun and the outcome of the algorithms discussed above. The Arduino may also be instructed to stop rotation if the sun is already centered in frame.

# Streaming
While not the primary focus of the project, the Pi simultaneously streams captured footage following a simple client-server model. The server script is run on a ground station laptop. The Pi sends video data via UDP packets to this ground station via a high-throughput Ubiquiti LAN. The team uses UDP rather than TCP as a transport-layer protocol due to its reduced overhead and connectionless architecture (connectivity is not guaranteed during flight as the balloon moves in unpredictable ways during flight).

# Testing
To run pytests, execute the following command from the
directory containing the modules to-be-tested:
```
python -m pytest
```

Pytest can be installed using pip:
```
pip install -U pytest
```

