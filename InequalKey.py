#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 00:27:06 2022

@author: nix
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
outname = rounds+"_"+name+'_Discarded_NoEve.csv'
f = open(outname, 'w')
writer = csv.writer(f)
# writer.writerow(['Discarded Bits','Eves Knowledge A','Eves Knowledge B'])
writer.writerow(['Discarded Bits'])
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
# plotting.plot_DisBits(outname)