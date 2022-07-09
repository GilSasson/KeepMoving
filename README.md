# Keep Moving
Sensing system design and algorithm development for balance decline detection and intervention in the elderly

# Project report
 - Final report.pdf
 - Semester report.pdf
 - Project Slides.pptx

# Operating system, etc
- Linux ubuntu 18.04
- ROS Melodic
- Python 2.7

# Main files
## Python code
sub.py
## Catkin file
catkin.zip can be downloaded via Google drive using the following link
https://drive.google.com/file/d/1bGJ6LfMC1pHTB_K_3XD3Iwmnz_NFeAm7/view?usp=sharing
## hdl_people_tracking modified parameters
hdl_people_tracking_static.launch

# Solidworks LiDAR mount
- LidarMountPart1.SLDPRT
- Part2.SLDPRT
- LiDAR.SLDPRT

#  

# LSTM model
 Check out the LSTM_test.ipynb colab. We advise to take more data using the LiDAR at different distances as discussed in the final report.
 - Current LSTM model uses data from lidar_test.csv file.
 
# Kenji Koide's people tracking can be found here
https://github.com/koide3/hdl_people_tracking

## Our modified hdl_people_tracking parameters for the Leishen Intelligence System 16C LiDAR
Download the hdl_people_tracking file. We advise to change these paramters for better results in the future or use Koide's
paramters if using 32 layered Velodyne LiDAR. Note that changing these may require to change the HPF threshold in the Sub.py file
for calculating the correct distance traveled and velocity (i.e. to remove to noise properly). 

# Consumer survey
https://docs.google.com/forms/d/e/1FAIpQLSfcfyJ6ekp1y2lQ_J2TugChexLEdf3k7uKT_kq6_L6l1LB5Qw/viewform

# Poster 
![](https://github.com/GilSasson/KeepMoving/blob/main/Poster.jpeg?raw=true)
