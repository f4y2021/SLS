#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
os.chdir("C:/dataset")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import re
import sys


# In[2]:


dfname=pd.ExcelFile("SLS_Adhesive_Results3.xlsx")
print(dfname.sheet_names)


# In[46]:


first_choice="C11"
second_choice="C11"
graph_select=first_choice+"_"+second_choice
print(graph_select)


# In[47]:


df_aux=pd.read_excel("SLS_Adhesive_Results3.xlsx",sheet_name=graph_select,usecols= [0,1,3,4,6,7,9,10,12,13],header=0,
                     names=["S1_d","S1_f","S2_d","S2_f","S3_d","S3_f","S4_d","S4_f","S5_d","S5_f"])


# In[48]:


df_chosen=df_aux.dropna()
print(df_chosen)


# In[49]:


ax = plt.gca()
for i in range (1,6):
    df_chosen.plot(ax=ax,x="S"+str(i)+"_d",y="S"+str(i)+"_f")
plt.show()


# In[ ]:





# In[ ]:




