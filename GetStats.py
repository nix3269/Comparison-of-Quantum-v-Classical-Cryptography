#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 14:09:52 2022

@author: nix
"""
import numpy as np
import pandas as pd
import csv
import sys

df = pd.read_csv("100_ECDH_data.csv")

# readdata = csv.reader(open(, 'r'))
# data = []

dset = list(df['Time usage'])

print("Mean:" +str(np.mean(dset))[:6])
print("Median: "+str(np.median(dset))[:6])
print("Average: "+str(np.average(dset))[:6])
print("Standard Variance: "+str(np.std(dset))[:6])

# for row in readdata:
#   data.append(row)

# #incaMse you have a header/title in the first row of your csv file, do the next line else skip it
# data.pop(0) 

# q1 = []  

# for i in range(len(data)):
#   q1.append(data[i][0])

# print ('Mean of your_column_number :            ', (np.mean(q1)))