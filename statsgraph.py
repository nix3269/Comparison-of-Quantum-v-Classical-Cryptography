#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 18:44:32 2022

@author: nix
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import statistics

def Stats(dset):
    print("Median is ",np.median(dset))
    print("Average is ",np.average(dset))
    print("Standard is ",type(np.std(dset)))
    
    return([np.median(dset),np.average(dset),np.std(dset)])


itrlist='BitSim1.csv BitSim2.csv'
namelist, avg, median, std=['Without Eve', 'With Eve'], [], [], []
for i in itrlist.split(" "):
    filename = i
    df = pd.read_csv(filename, error_bad_lines=False)
    arr = Stats(df)
    avg.append(arr[1])
    std.append(arr[2])
    median.append(arr[0])
y_pos = np.arange(len(namelist))
bar_colors = ['tab:red', 'tab:blue']
fig, ax = plt.subplots()
ax.bar(namelist, avg, label=namelist, color=bar_colors)
ax.set_title('Average Bit Similarity between Alice and Bob (BB84)')

# df = pd.read_csv("BB84EveKnow.csv", error_bad_lines=False)
# Stats(df)

plt.show()