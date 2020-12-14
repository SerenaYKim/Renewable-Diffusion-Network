# -*- coding: utf-8 -*-
"""Renewable-Diffusion-Network-Similarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15WUUCISv5Xk5XeOfUM1eOciXdxk4P0jd
"""

gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
if gpu_info.find('failed') >= 0:
  print('Select the Runtime > "Change runtime type" menu to enable a GPU accelerator, ')
  print('and then re-execute this cell.')
else:
  print(gpu_info)

from psutil import virtual_memory
ram_gb = virtual_memory().total / 1e9
print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

if ram_gb < 20:
  print('To enable a high-RAM runtime, select the Runtime > "Change runtime type"')
  print('menu, and then select High-RAM in the Runtime shape dropdown. Then, ')
  print('re-execute this cell.')
else:
  print('You are using a high-RAM runtime!')

import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
import numpy as np
import itertools as iter
from random import sample
from itertools import chain 
import csv
import glob
import os
from numpy.random import poisson #import
import pickle
import scipy
from scipy import stats
from functools import reduce
import operator

df_edge = pd.read_csv('/content/drive/MyDrive/G11-MEA-Diffusion/dataSim_Lang/edges_reduced_v3.csv')
df_weights = pd.merge(df_edge, df_edge, on='language', suffixes=['','2']).query("country != country2")
df_weights.drop(df_weights.loc[df_weights['country'] > df_weights['country2']].index, inplace=True)

df_weights = df_weights.sort_values(by=['country'])
df_weights["node_pair"] = df_weights["country"].apply(str) + ", " + df_weights["country2"].apply(str)
df_weights["lang_sim"] = df_weights["weight"] * df_weights["weight2"] 
df_weights = df_weights.sort_values(by=['node_pair'])

crosstab = df_weights.groupby(['node_pair'])['lang_sim'].sum().reset_index()

edge_lang = pd.DataFrame() 
edge_lang[['node1','node2']] = crosstab.node_pair.str.split(", ",expand=True,)
edge_lang['node1']=edge_lang['node1'].astype(str).astype(int)
edge_lang['node2']=edge_lang['node2'].astype(str).astype(int)
edge_lang['lang_sim'] = crosstab['lang_sim']

ctry = pd.read_csv('/content/drive/MyDrive/G11-MEA-Diffusion/dataSim_Lang/node_list_reduced_v3.csv')
ctry_lst = list(ctry["countrycode"])
G_lang = nx.from_pandas_edgelist(edge_lang, source='node1', target='node2', edge_attr='lang_sim', create_using=None, edge_key=None)
lang_adj = nx.adjacency_matrix(G_lang)
lang_adj = nx.to_numpy_matrix(G_lang, nodelist=ctry_lst, weight='lang_sim')

df_lang_adj = pd.DataFrame(data=lang_adj)
df_lang_adj['0'] = ctry_lst
cols = df_lang_adj.columns.tolist() # the order of columns mixed for some reason 
cols = cols[-1:] + cols[:-1]  # column order fixed
df_lang_adj = df_lang_adj[cols]

lang_w_matrix = df_lang_adj.to_numpy()

np.savetxt('/content/drive/MyDrive/G11-MEA-Diffusion/dataSim_Lang/langwv3.txt', lang_w_matrix, fmt='%.3f')

from_networkx(graph, weight_col='weight')

listsdf = [3,4,5,6,7,8,9]
listsdf[:-1]

num_rows, num_cols = df_lang_adj.shape
print (num_rows, num_cols)



num_rows, num_cols = A.shape
print (num_rows, num_cols)

np.savetxt('/content/drive/MyDrive/G11-MEA-Diffusion/dataSim_Language/lang_w.txt',A,fmt='%.4f')