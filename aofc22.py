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
z_path ='/Users/marc.fabel/projects/adventofcode2022/data/'

# magic numbers




###############################################################################
#   Day 6: Tuning Trouble
###############################################################################

# define characters to be processed before the first start-of-message marker is detected
marker_length = 14 # Part 1: 4 | Part 2: 14

with open(z_path + '6.txt', 'r') as file:
    s = file.read()

# convert string to list of characters
s = list(s)

j_start = 0

while j_start < len(s):
    j_end = j_start + marker_length
    export = s[j_start: j_end]
    
    # count occurences
    count = []
    for element in export:
        count.append(export.count(element))
        
    # duplicate entries - increase start by one
    if max(count) > 1:
        j_start = j_start +1
        
    else:
        print('finished, answer: ', j_start + marker_length)
        j_start = len(s)



###############################################################################
#   Day 5: Supply Stacks
###############################################################################
def top_crates_stack(dict):
    result = []
    for k in dict.keys(): 
        result.append(dict[k][-1])
    return ''.join(result)


# Part 1 ######################################################################
# reverse order of pick-up stack

stacks = pd.read_csv(z_path + '5_stack.txt', sep=',', header=None)
stacks.columns = stacks.columns + 1
stacks = stacks.sort_index(ascending=False)
stacks = stacks.to_dict('list')
# remove empty spaces: 
for k in [1,4,5,6,7,9]:
    stacks[k] = list(filter(lambda a: a != ' ', stacks[k]))
    
    

# get procedures
df = pd.read_csv(z_path + '5.txt', sep=' ', names=['x', 'qty', 'y', 'o', 'z', 'd'])
df.drop(['x','y', 'z'], axis=1, inplace=True)
    
    
# cary out instructions
row = 0
while row < len(df):
    qty, o, d =  df.iloc[row]['qty'], df.iloc[row]['o'], df.iloc[row]['d']
    
    # pick up - and reverse order
    pick_up = stacks[o][-qty:]
    pick_up.reverse()
    
    # add to destination
    for j in pick_up:
        stacks[d].append(j)
    
    # remove from origin
    stacks[o] = stacks[o][:-qty]
    row = row+1

# print top crates per stack
top_crates_stack(stacks)




# Part 2 ######################################################################
# same as before - just remove the reverse ordering from the pick_up variable

stacks = pd.read_csv(z_path + '5_stack.txt', sep=',', header=None)
stacks.columns = stacks.columns + 1
stacks = stacks.sort_index(ascending=False)
stacks = stacks.to_dict('list')
# remove empty spaces: 
for k in [1,4,5,6,7,9]:
    stacks[k] = list(filter(lambda a: a != ' ', stacks[k]))
        
    
    
# cary out instructions
row = 0
while row < len(df):
    qty, o, d =  df.iloc[row]['qty'], df.iloc[row]['o'], df.iloc[row]['d']
    
    # pick up - NOT reverse order
    pick_up = stacks[o][-qty:]
    # pick_up.reverse()
    
    # add to destination
    for j in pick_up:
        stacks[d].append(j)
    
    # remove from origin
    stacks[o] = stacks[o][:-qty]
    row = row+1

# print top crates per stack
top_crates_stack(stacks)




###############################################################################
#   Day 4: Camp Cleanup
###############################################################################

df = pd.read_csv(z_path + '4.txt', names=['a1','a2'], sep=',')

# Part 1 - how many pairs contain each other assignments ######################

# have lower and upper bound of assignments in seperate columns
df[['a1l','a1h']] = df['a1'].str.split('-', expand=True).astype(int)
df[['a2l','a2h']] = df['a2'].str.split('-', expand=True).astype(int)

# dummy - one assignment fully contains the other
df['d_fully_contained'] = np.where(
    # a1 contained in a2
    ((df['a1l'] >= df['a2l']) & (df['a1h']<=df['a2h'])) |
    
    ((df['a2l'] >= df['a1l']) & (df['a2h']<=df['a1h'])),
    1,0)

print(df['d_fully_contained'].sum())


# Part 2 - number of pairs that overlap at all ################################

# dummy - is there an overlap of one assignment with the other
df['d_overlap'] = np.where(
    ((df['a1h']>=df['a2l']) & (df['a1l']<=df['a2l'])) |
    ((df['a2h']>=df['a1l']) & (df['a2l']<=df['a1l'])),
    1,0 )

print(df['d_overlap'].sum())



###############################################################################
#   Day 3 Rucksack Reorganization
###############################################################################


# General Setup ###############################################################
# define Ditionaries with points
import string
dict_lc = dict(zip(string.ascii_lowercase, range(1,27)))
dict_up = dict(zip(string.ascii_uppercase, range(27,53)))
dict_points = dict_lc.copy()
dict_points.update(dict_up)


# Part 1 - identify common elements in two compartments per rucksack ##########
df = pd.read_csv(z_path + '3.txt', names=['rs'])

# split rucksacks in two compartments
df['comparment_length'] = (df['rs'].str.len() /2).astype(int)
df['rs'].str.slice(0, df['comparment_length'])
df['cmprmnt1'] = df.apply(lambda row: str(row['rs'])[:row['comparment_length']],
                          axis=1)
df['cmprmnt2'] = df.apply(lambda row: str(row['rs'])[row['comparment_length']:],
                          axis=1)

# points for common element
df['common_element'] = df.apply(lambda row:
                                list(set(row['cmprmnt1']).intersection((row['cmprmnt2'])))[0],
                                axis=1)
df['points_common_element'] = df['common_element'].map(dict_points)
print(df['points_common_element'].sum())


# Part 2 - Group Level ########################################################
df['group'] = (((df.index ) // 3) + 1)
df['count'] = df.groupby(['group']).cumcount()+1

# reshape to have elements on group level
group_level = pd.pivot(df, index='group', values='rs', columns='count')

# common element
group_level['common_element'] = group_level.apply(lambda row:
                                list(
                                    set(row[1]).intersection(row[2]).intersection(row[3])
                                    )[0],
                                axis=1)

group_level['points_common_element'] = group_level['common_element'].map(dict_points)
print(group_level['points_common_element'].sum())
		
    


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
