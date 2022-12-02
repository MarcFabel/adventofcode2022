#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 09:34:30 2022

@author: marc.fabel

Description:
    xxx
    
Inputs:
    none
    
Outputs:
    none
    
Updates:
    none
"""

# packages
import pandas as pd
import numpy as np

# paths
z_path ='/Users/marc.fabel/projects/adventofcode22/data/'

# magic numbers




###############################################################################
#   Day 1
###############################################################################
calories = pd.read_csv(z_path + '1.txt',skip_blank_lines=False, names=['calories'])

# generate elfe counter
calories['elf'] = np.where(calories.calories.isnull(),1,0)
calories['elf'] = calories['elf'].cumsum()
calories['elf'] = calories['elf'] + 1
calories.dropna(inplace=True)

total = calories.groupby(by='elf').sum()



###############################################################################
#   Day 2 - Rock Paper Sicors
#######################################################################


# Second Column means how I Should respond ####################################

# open stratgey guide
df = pd.read_csv((z_path + '2.txt'), sep=' ', names=['opp', 'response'])

# reeconde ABC, AYC
df = df.replace({'A':'R', 'B':'P', 'C':'S', 'X':'R', 'Y':'P','Z':'S'})

z_dict_shape_points = {'R':1, 'P':2, 'S':3}


df['points_shape'] = df['response'].map(z_dict_shape_points)

# points outcome of game
# A) Draw
df['points_outcome'] = np.where(df['opp']==df['response'], 3, -1)
# B) Win
df.loc[
       ( (df['response']=='R') & (df['opp']=='S') ) |
       ( (df['response']=='S') & (df['opp']=='P' )) |
       ( (df['response']=='P') & (df['opp']=='R' )) 
       , 'points_outcome'] = 6

# loss
df.loc[df['points_outcome']==-1, 'points_outcome'] = 0


df['total'] = df['points_shape'] + df['points_outcome']
print(df['total'].sum())



# Second Column means how round needs to end ##################################
df = pd.read_csv((z_path + '2.txt'), sep=' ', names=['opp', 'outcome'])
df = df.replace({'A':'R', 'B':'P', 'C':'S'})

# A) Draw-> response is Draw
df['response'] = np.where(df['outcome']=='Y', df['opp'], -1)

# B) Loss (outcome=X)
df.loc[(df['outcome']=='X') & (df['opp']=='R'), 'response'] = 'S'
df.loc[(df['outcome']=='X') & (df['opp']=='S'), 'response'] = 'P'
df.loc[(df['outcome']=='X') & (df['opp']=='P'), 'response'] = 'R'

# C) Win (outcomeZ)
df.loc[(df['outcome']=='Z') & (df['opp']=='R'), 'response'] = 'P'
df.loc[(df['outcome']=='Z') & (df['opp']=='S'), 'response'] = 'R'
df.loc[(df['outcome']=='Z') & (df['opp']=='P'), 'response'] = 'S'


df['points_shape'] = df['response'].map(z_dict_shape_points)
df['points_outcome'] = df['outcome'].map({'X':0, 'Y':3, 'Z':6})

df['total'] = df['points_shape'] + df['points_outcome']
print(df['total'].sum())
