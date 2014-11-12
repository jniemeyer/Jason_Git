# -*- coding: utf-8 -*-
"""
This program plots and finds statics for P1 bond coupon test data.
Test data is output from LabView

Created on Fri Nov 07 13:35:26 2014

@author: rsmcclel
"""

import numpy as np
import matplotlib.pyplot as plt
import os

data_path = "Helena_Data/1.8 mm Test 6-25-13"

def get_data_paths(data_path):
    # Returns a list of the text files within the directory data_path    
    txt_paths = []
    for root, dirs, files in os.walk(data_path):
        for f in files:
            if os.path.splitext(f)[1] == ".txt":
                txt_paths.append(os.path.join(root, f))
    return txt_paths
    
txt_paths = get_data_paths(data_path)

def find_yield(disp, moment):
    # Find the yield by iterating until the residual is greater than desired    
    for x in range(len(disp)/2,len(disp)):      
        # Fit a line to more data, until it becomes too non linear        
        residual = np.polyfit(disp[:x], moment [:x],1, True)[1]
        if residual > 3.3:  # Hard code residual limit         
            return disp[x], moment[x]
            break
        elif x == len(disp)-1:  # If residual isn't exceeded, use maximum moment
            return disp[x], moment[x]

# Initilize lists for summary data from all trails
max_all = []
yield_all = []

for data_file in txt_paths: 
    # Load  the data files
    time,disp,force,moment,max_force,disp_at_max = np.loadtxt(data_file, delimiter="\t", skiprows=24, unpack=True)
    # time in seconds, force in lbs, moment in N*mm
    disp = np.arctan(disp/10)  # Convert from displacement to angle assuming 10 mm offest
    trim_beg = np.argmax(moment>moment.max()*.03)  # Trim begging of data at 5% of max
    trim_end = moment.argmax() # Trim end at maximum
    disp = disp - disp[trim_beg] # Normalize the displacements to same starting disp
    # Plotting
    plt.title('P1 Coupon Test Data')
    plt.ylabel('Moment (N*mm)')
    plt.xlabel('Displacement (mm)')    
    plt.plot(disp[trim_beg:trim_end],moment[trim_beg:trim_end], label=os.path.split(data_file)[1])
    plt.legend(loc=0)
    
    # Find and plot yield point
    yield_disp, yield_moment = find_yield(disp[trim_beg:trim_end],moment[trim_beg:trim_end])
    plt.plot(yield_disp,yield_moment,"or")
    # Store summary data from each file
    max_all.append(moment.max())
    yield_all.append(yield_moment)
    
# Plot stats
max_avg = np.average(max_all)
max_std = np.std(max_all)
yield_avg = np.average(yield_all)
yield_std = np.std(yield_all)
stat_label0 = ('Max moment avg {:.2f} N*mm'.format(max_avg) + 
        ', std dev {:.2f} N*mm'.format(max_std) + '\n')
stat_label1 = ('Yield moment avg  {:.2f} N*mm'.format(yield_avg) + 
        ', std dev {:.2f} N*mm'.format(yield_std) + '\n')
plt.suptitle(stat_label0 + stat_label1)