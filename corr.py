#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 02:44:06 2022

@author: nix
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 17:18:03 2022

@author: Nix
"""

import time;
import csv;
import sys
from io import StringIO
import contextlib
import plotting

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

rounds = sys.argv[1]
filename = sys.argv[2]
name, ext= filename.split(".")
outname = rounds+"_"+name+'_Corr_WithEVE_data.csv'
f = open(outname, 'w')
writer = csv.writer(f)
writer.writerow(['CHSH correlation value'])
print(rounds, filename)
for i in range(int(rounds)):
    print(i);
    with stdoutIO() as s:
        try:
            exec(open(filename).read())
            row = [float(s.getvalue().split("\n")[0])]
            print(row)
            writer.writerow(row)
        except:
            print("Something wrong with the code")
f.close()
plotting.plot_Corr(outname)