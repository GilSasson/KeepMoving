#!/usr/bin/env python

from timeit import default_timer as timer
from std_msgs.msg import String
from visualization_msgs.msg import MarkerArray
from datetime import date
import time
import rospy
import numpy as np 
import math
import pandas as pd
from scipy import stats
import csv

todays_date = date.today()
positionx = []
positiony = []
positionz = []
avgpositionx = []
avgpositiony = []
avgpositionz = []
t_start=time.time() #to count time for person in room and substract time when not in room (time "stops" if not in room)
t_startmonth=time.time()

t1=0 #time reference
month = todays_date.month #will be used in callback to save current month
MRT = [] #Monthly Room Time
distance = 0
distance_z = 0
distance_M = []
velocity = 0
velocity_M = []
distance_z_M = []
velocity_z_M = []
distance_month = []
t2=0 #for speed/acceleration time reference


def callback(data):
    global t_start, t_startmonth, t1, month, distance
    if(len(data.markers)>1):
        t_start_dist=time.time()
        positionx.append(data.markers[1].pose.position.x)
        positiony.append(data.markers[1].pose.position.y)
        positionz.append(data.markers[1].pose.position.z)

        #---TREMOVING OUTLIERS THIS PART REQUIRES MORE RESEARCH---
        # #Setting up DataFrames
        # df1 = pd.DataFrame({'distance_col': positionx[-25:]})
        # df2 = pd.DataFrame({'distance_col': positiony[-25:]})
        # df3 = pd.DataFrame({'distance_col': positionz[-25:]})
        # #Removing outliers from the coordinates x,y,z
        # filtered_posx = remove_outliers(df1)
        # filtered_posy = remove_outliers(df2)
        # filtered_posz = remove_outliers(df3)
        # --------------------------------------------------------

        if len(positionx) > 25:
            avgpositionx.append(np.sum(positionx[-25:])/25)
            avgpositiony.append(np.sum(positiony[-25:])/25)
            avgpositionz.append(np.sum(positiony[-25:])/25)
            # avgpositionx.append(np.sum(filtered_posx[-25:])/25) #REMOVE OUTLIERS
            # avgpositiony.append(np.sum(filtered_posy[-25:])/25) #REMOVE OUTLIERS
            # avgpositionz.append(np.sum(filtered_posz[-25:])/25) #REMOVE OUTLIERS
        t1=time.time()-t_start
        distance = EuclideanDistance(avgpositionx,avgpositiony,distance)
        distance_M.append(distance)
        distance_vector = distance_M[-25:-1]
        t2=time.time()-t_start_dist
        velocity = (distance_M[-1]-distance_M[-2])/(t2*100)
        velocity_M.append(velocity)
        distance_z = avgpositionz[-1]
        distance_z_M.append(distance_z)
        velocity_z = (avgpositionz[-1]-avgpositionz[-2])/(t2*100)

        #Setting up DataFrames
        outliers = 0
        if len(distance_z_M) > 100:
            df1 = pd.DataFrame({'distance_col': distance_z_M[-100:]})
            outliers = remove_outliers(df1)

        print(outliers)
        print("velocity_z is", velocity_z)
        print("distance_z is",distance_z)
        print("distance is",distance)
        print("velocity is",velocity)
        print("The total time in the room is:",time.time()-t_start, "seconds.")
        print("len of markers is ",len(data.markers))       
        with open('test.csv', 'a') as csvfile:
            fieldnames = ['time', 'distance_z', 'velocity_z', 'outliers']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'time': time.time()-t_start, 'distance_z': distance_z, 'velocity_z': velocity_z, 'outliers': outliers})
        
        # Monthly graphs and data
        # t1=time.time()-t_start
        # t_startmonth=time.time()
        # distance_month = []
        # MRT = []
        # distance = EuclideanDistance(avgpositionx,avgpositiony,distance)
        if(time.time()-t_startmonth < 2629744.1005 and time.time()-t_startmonth > 2629743.633): # avg time each month 
            month = todays_date.month # saving current month
            MRT.append(time.time()-t_start) # monthly room time
            distance_month.append(distance) # monthly room distance
            if len(distance_month) > 1:
                monthly_distance = distance_month[-1] - distance_month[-2]
            else:
                monthly_distance = distance_month[-1]
            print("The total distance traveled in month", month, "is:", monthly_distance)
            print("The average velocity in month", month, "is:", np.mean(velocity_M))
            print("The total time in the room in month", month, "is: ", MRT[-1], "seconds.")  
            time_startmonth = time.time() # resetting month time to recount the time until next month prints


        
    else: #if(len(data.markers) <= 1)
        t_start=time.time()-t1 #when person not in room


def remove_outliers(df):

    # First we will filter "far" outliers using IQR method. Secondly, using Z-score method, we will filter
    # abnormal measurements e.g. in the following vector; u = [60.2, 61.2, 20.2, 62.9, ...]
    # the measurement  u[2] = 20.2 is considered abnormal.

    # 'nan' outliers out-side of the lower/upper bound
    for j in ['distance_col']:
        q_75, q_25 = np.percentile(df.loc[:, j], [75, 25])
        inter_qr = q_75 - q_25
        maxima = q_75 + (1.5 * inter_qr)  # upper-bound
        minima = q_25 - (1.5 * inter_qr)  #s lower-bound
        df.loc[df[j] < minima, j] = np.nan
        df.loc[df[j] > maxima, j] = np.nan
        null_counter = df.distance_col.isnull().sum() #test
        df_n = df.dropna(axis=0)  # Removing nans

        # Creating a new array of the differences i.e. distance_col [j+1] - distance_col [j]
        # and then usingdistance_vector = distance_M[-25:-1] standard score we shall define the outliers.
        d = np.array(df_n['distance_col'])
        d_diff = np.diff(d)
        z = stats.zscore(d_diff)
        threshold = 3  # Standard deviation
        # Position of the outlier
        outlier_pos = np.where(z > threshold)
        outlier = d[outlier_pos]
        for j in ['distance_col']:
            for k in range(0, len(outlier)):
                df.loc[df[j] == outlier[k], j] = np.nan
        df = df.dropna(axis=0)  # Removing nans
        d_n = np.array(df['distance_col'])
        null_counter_2 = null_counter + df.distance_col.isnull().sum() #test
        if null_counter > 22: #threshold for almost-fall criterion
            return 1
        else:
            return 0


def EuclideanDistance(x,y,distance):
    addition = 0
    num1=x[-1]
    num2=x[-2]
    num3=y[-1]
    num4=y[-2]
    addition = math.sqrt(pow(num1-num2,2)+pow(num3-num4,2))
    if (addition > 0.008 and addition < 2): #from experiments 
        distance += addition
    return distance


def main():
    with open('test.csv', 'w') as csvfile:
        fieldnames = ['time', 'distance_z', 'velocity_z', 'outliers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    rospy.init_node('main', anonymous=True)
    rospy.Subscriber('hdl_people_tracking_nodelet/markers',MarkerArray, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    main()






