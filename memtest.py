# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 19:14:33 2022

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

inp = input("Enter Number of rounds and Filename! Thanks :)")
rounds, filename = inp.split(" ")
name, ext= filename.split(".")
outname = rounds+"_"+name+'_Memory-data.csv'
f = open(outname, 'w')
writer = csv.writer(f)
writer.writerow(['Memory usage'])
print(rounds, filename)
for i in range(int(rounds)):
    print(i)
    with stdoutIO() as s:
        try:
            exec(open(filename).read())
        except:
            print("Something wrong with the code")
    row = [int(s.getvalue().split("\n")[0])]
    writer.writerow(row)
f.close()
plotting.plot_Memory(outname)