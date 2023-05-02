#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 00:27:06 2022

@author: nix
"""

import csv;
import sys
from io import StringIO
import contextlib

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
    
def know():
    rounds = sys.argv[1]
    filename = sys.argv[2]
    name, ext= filename.split(".")
    outname = rounds+"_"+name+'_Eve_Knowledge_BB84.csv'
    f = open(outname, 'w')
    writer = csv.writer(f)
    writer.writerow(['Discarded Bits','Eves Knowledge A','Eves Knowledge B'])
    print(rounds, filename)
    for i in range(int(rounds)):
        print(i);
        with stdoutIO() as s:
            try:
                exec(open(filename).read())
                row = [float(s.getvalue().split("\n")[0]),float(s.getvalue().split("\n")[1]),float(s.getvalue().split("\n")[2])]
                print(row)
                writer.writerow(row)
            except:
                print("Something wrong with the code")
    f.close()

# rounds = '5'
# filename = "BB84withEVE.py"
# name, ext= filename.split(".")
# outname = rounds+"_"+'_BitSimilarity_BB84.csv'
f = open("BitSim1.csv", 'w')
writer = csv.writer(f)
writer.writerow(['Without Eve', 'With Eve'])
for i in range(int(1000)):
    print(i);
    with stdoutIO() as s:
        try:
            exec(open("BB84withEVE.py").read())
        except:
            print("Something wrong with the code")
        row = [float(s.getvalue().split("\n")[0]), float(s.getvalue().split("\n")[1])]
        print(row)
        writer.writerow(row)
f.close()