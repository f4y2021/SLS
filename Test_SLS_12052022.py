"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
#Formatar Ficheiro Excel
import openpyxl
import plost
import plotly.express as px 
import plotly.graph_objects as go

import streamlit as st

import numpy as np
import pandas as pd

import re
import sys

first_choice = st.selectbox('Select Sample #1',('C11', 'C12', 'C21', 'C22'))
second_choice = st.selectbox('Select Sample #2',('C11', 'C12', 'C21', 'C22'))
graph_select=first_choice+"_"+second_choice
st.write('You selected:', graph_select)

#excel_data=st.file_uploader("Choose data file")

run_button=st.button("Run")

if run_button:

  df_aux=pd.read_excel("./data/SLS_Adhesive_Results3.xlsx",sheet_name=graph_select,usecols= [0,1,3,4,6,7,9,10,12,13],header=0,names=["S1_d","S1_f","S2_d","S2_f","S3_d","S3_f","S4_d","S4_f","S5_d","S5_f"])

  df_chosen=df_aux.dropna()
  st.dataframe(df_chosen)
  fig = px.line(df_chosen, x=df_chosen.columns[0], y=df_chosen.columns[1])
  for i in range (3,13,3):
    fig.add_trace(go.Scatter(x="df_chosen.columns[i]", y="df_chosen.columns[i+1]"))

  st.plotly_chart(fig)





