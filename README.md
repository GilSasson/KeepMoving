# KeepMoving
Sensing system design and algorithm development for balance decline detection and intervention in the elderly

# Project report
 - Final report.pdf
 - Semester report.pdf
# Operating system, etc
- Linux ubuntu 
- ROS Melodic
- Python 2.7

# Python file
Sub.py

# Solidworks LiDAR mount
Files: Mount_part_1, Mount_part_2

#  

# LSTM model
 check out the LSTM test colab. We advise to take more data using the LiDAR at different distances as discussed in the final report.
 - Current LSTM model uses data from lidar_test.csv file.
 
# Kenji Koide's people tracking can be found here
https://github.com/koide3/hdl_people_tracking

## Our modified hdl_people_tracking parameters for the Leishen Intelligence System 16C LiDAR
download the hdl_people_tracking file. we advise to change these paramters for better results in the future or use Koide's
paramters if using 32 layered Velodyne LiDAR. Note that changing these may require to change the HPF threshold in the Sub.py file
for calculating the correct distance traveled and velocity (i.e. to remove to noise properly). 

