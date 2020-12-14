#!/usr/bin/env python
# coding: utf-8

# ### Import

# In[82]:


import bs4 as bs
import urllib.request
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from random import sample
from itertools import chain 
import csv
import glob
import os
from functools import reduce


# ### Parsing Data from International Environmental Agreement Database (IEADB)

# In[80]:


# Metadata includes all MEAs signed from 2000 

iea_meta = pd.read_csv("iea_meta.csv")
iea_list=[]
for column in iea_meta.columns: 
    iea_list = iea_meta["iea"].tolist() 


# In[69]:


df_all = []

# Iterate using the iea_list
for i in iea_list:
    k = str(i) 
    dfs = pd.read_html('https://iea.uoregon.edu/membership-long-form/'+k+'/long', header=0)
    for df in dfs:
        df['iea'] = i
        df_all.append(df)
df_all = pd.concat(df_all)

# It took about 10 minutes
print("DONE")


# In[93]:


# Keep a copy (just in case)
df_all_copy = df_all


# In[94]:


# Delete blank cells 
index_void = df_all[ df_all['Country'] == "No results"].index
df_all.drop(index_void, inplace=True)

# Delete times before an agreement was in effect
df_all = df_all[df_all['Membership Status'] != 0]

# Sort the columns in the following order 
df_all= df_all.sort_values(by=['Country', 'Year', 'iea', 'Membership Status'])


# In[95]:


# Merging 
frame = [df_all, iea_meta]
df_merged = reduce(lambda  left, right: pd.merge(left,right,on=['iea'],
                                            how='outer'), frame).fillna('0')

# Deleted observations that are only in the iea_meta 
df_merged = df_merged [df_merged ['Country'] != "0"]

# Sort and clean 
df_merged = df_merged.drop(columns=['Inclusion', 'Signature Year', 'Signature Date', 'Treaty Text', 'Members', 'Data'])
df_merged = df_merged.sort_values(by=['Country', 'Year', 'iea', 'Membership Status'])

# Export
df_merged.to_csv('MEA_List.csv')


# #### Done!
