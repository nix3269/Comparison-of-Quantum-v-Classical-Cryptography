# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 17:18:03 2022

@author: Nix
"""

import time;
import csv;
import plotting

inp = "30 RSA.py"
rounds, filename = inp.split(" ")
name, ext= filename.split(".")
outname = rounds+"_"+name+'_data.csv'
f = open(outname, 'w')
writer = csv.writer(f)
print(rounds, filename)
for i in range(int(rounds)):
	now = time.time()
	exec(open(filename).read())
	after = time.time()
	row = [now, after,after-now]
	writer.writerow(row)
f.close()
plotting.plot_line(outname)