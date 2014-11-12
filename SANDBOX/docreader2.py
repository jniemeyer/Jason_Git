# -*- coding: utf-8 -*-
"""
This app will read in a file and do some analysis on it (hopefully)

Created on Mon Nov 10 09:02:10 2014

@author: jniemeye
"""
import numpy as np
import matplotlib.dates as dates
import matplotlib.pyplot as plt
from datetime import datetime
import os

#Start of experimental section
data_path = "SANDBOX"

def get_data_paths(data_path):
    # Returns a list of the text files within the directory data_path    
    txt_paths = []
    for root, dirs, files in os.walk(data_path):
        for f in files:
            if os.path.splitext(f)[1] == ".txt":
                txt_paths.append(os.path.join(root, f))
    return txt_paths
    
txt_paths = get_data_paths(data_path)

for data_file in txt_paths:
    #End of experimental section
    
    #Opens the data file
    
    f = open(data_file, 'r')
    
    original = data_file
    split1 = original.split('/')
    split2 = split1[7].split('_')
    
    
    mp = split2[0]
    mirror = split2[1]
    side = split2[2]
    pin = split2[3]
    
    time = []; force = []; cds = []; limit = []
    
    header1 = f.readline() #Skips past the first header line
    header2 = f.readline() #Skips past the second header line
    lines = f.readlines() #Reads in remainder of lines
    f.close()
    
    splitlines = [] #Variable which will store the split "tab delimited" data
    
    for line in range(len(lines)):
        split = lines[line].split('\t')
        for x in range(len(split)):
            splitlines.append(split[x])
        limit.append(6)
    
    count = 0
    
    for x in range(len(splitlines)):
        if count == 0:
            time.append(splitlines[x])
            count += 1
        elif count == 1:
            force.append(float(splitlines[x]))
            count += 1
        elif count == 2:
            cds.append(float(splitlines[x]))
            count = 0
    
    count = 0        
    
    time_objects = []
    
    for x in range(len(time)):
        splittime = time[count].split(':')
        for y in range(len(splittime)):            
            minute = int(splittime[0])
            second = int(splittime[1])
            microsecond = int(float(splittime[2]) * 1e6) 
        time_objects.append(datetime(2014, 1, 1, 0,minute, second, microsecond))
        count += 1
        
    times = dates.date2num(time_objects)
    times *= 86400
    
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.plot(times, force, 'g.', label = 'Force')
    ax1.plot(times, limit, 'b:', label = 'Force Threshold')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Force (mN)')
    ax2 = ax1.twinx()
    ax2.plot(times, cds, 'r', label = 'CDS')
    ax2.set_ylabel('Distance (microns)')
    ax1.legend(loc = 'upper left')
    ax2.legend(loc = 'lower left')
    plt.title('%s %s %s %s Mirror Detection' % (mp, mirror, side, pin))