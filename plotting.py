# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 21:47:49 2022

@author: Nix
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import statistics

def plot_line(filename):
    headers = ['X', 'Y']
    df = pd.read_csv(filename)
    # sns.histplot(df, linewidth=0);
    sns.displot(df, x="Memory usage", kde=True)
    # plt.show()