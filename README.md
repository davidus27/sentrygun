# Sentry Gun 
Sentry gun is my first big python project. It detects moving objects on camera and aims on them with laser beacon.

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Requirements](#Requirements)
* [Launch](#Launch)
* [License](#License)


## Introduction
It's a stationary Raspberry Pi acting as a Client and connected to the Server via static local IP address via Ethernet cable.
It identifies moving objects captured via a camera connected to the CSI connector on Raspberry Pi. The Client creates a session that constantly sends captured images. While the Server-side replies with the x and y-axis for servo motors. 

Based on the stream of data Server compares each captured image with the reference image that was created before movement.
Using Binary Threshold function the program builds individual contours of differences in the captured image and then calculates the center of the bigger object on camera. This center point is then sent back to the Raspberry Pi that uses them to aim at the detected object.


## Technologies
This project uses [OpenCV](https://opencv.org/) library for basic Computer Vision and Preprocessing of an image. ![OpenCv](images/opencv.png)


## Requirements
For the recreation of this project you neeed to have:

      Raspberry Pi (at least Model 2)
      CSI module camera (at least 7 Mpx)
      Servomotors connected to the GPIOPINOUTS
      Laser Beacon
      Accelrometer with ISP
      Computer with installed Python 3 and mentioned libraries
      3D printed model of the whole system
      Ethernet cable
      

## Launch

```
git clone https://github.com/davidus27/sentrygun/tree/master 
```


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
