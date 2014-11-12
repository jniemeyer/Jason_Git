# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 09:04:49 2014

@author: jniemeye
"""

import numpy as np
import matplotlib.pyplot as plt

x = range(30)
y = []
for i in range(len(x)):
    y.append(x[i]**2)
    
plt.plot(x, y)
    
