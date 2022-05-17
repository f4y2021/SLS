"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import openpyxl
import time
import plotly.express as px 
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import streamlit as st

from docx import Document

import numpy as np
import pandas as pd

import re
import sys

st.set_page_config(page_title="SLS Tests",page_icon="⏩")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    font-size:16px;font-weight:bold;height:2em;width:7em;
}
</style>""", unsafe_allow_html=True)

st.image('f4y_logo.png')

#st.markdown("<h1 style='text-align: center; font-size:48px;font-weight:bold;'>SLS Connection Analysis</h1>", unsafe_allow_html=True)

with st.expander("Considered Configurations"):
    st.image('./data/considered_configurations.png')
    
with st.expander("Specimen Geometry"):
    st.image('./data/specimen_geometry.png')

#connection_tech = st.checkbox('I know the connection technology I want to use')

col11, col22 = st.columns(2)
with col11:
    first_choice = st.selectbox('Select Substrate #1',('C11', 'C12', 'C21', 'C22'))
with col22:
    second_choice = st.selectbox('Select Substrate #2',('C11', 'C12', 'C21', 'C22'))

connection_tech=st.checkbox('I know Which Connection Technology I Want to Use')

connection_choice='Adhesive'

if connection_tech:
    connection_choice = st.selectbox('Select connection technology',('Bolt', 'Adhesive','Hybrid'))

excel_file_loc="./data/SLS_Results_"+connection_choice+".xlsx"

area=312.5

graph_select=first_choice+"_"+second_choice

#no_connection_tech = st.checkbox('Not Sure Which Connection Technology I Want to Use')
with st.container():
    st.write('You Selected:')
    if not connection_tech:
        st.write('All Connection Technologies between ', first_choice,'and',second_choice)
    else:
        st.write(connection_choice,'between',first_choice,'and',second_choice)

col111, col222, col333 = st.columns(3)

with col222:
    run_button=st.button("Run")

bolt_excel_file_loc="./data/SLS_Results_Bolt.xlsx"
hybrid_excel_file_loc="./data/SLS_Results_Hybrid.xlsx"
adhesive_excel_file_loc="./data/SLS_Results_Adhesive.xlsx"

if run_button:
    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.success('Done!')
    if not connection_tech:
        
        def arranjar(file_loc,sheet_loc,name):
            df_func=pd.read_excel(file_loc,sheet_name=sheet_loc,header=0,names=["S1_d","S1_f","S2_d","S2_f","S3_d","S3_f","S4_d","S4_f","S5_d","S5_f"])
            df_func = df_func.dropna(axis=0)
            df_func['S_d_'+name]=df_func[['S1_d','S2_d','S3_d','S4_d','S5_d']].mean(axis=1)
            df_func['S_f_'+name]=df_func[['S1_f','S2_f','S3_f','S4_f','S5_f']].mean(axis=1)
        
            return df_func
        
        df_bolt=arranjar(bolt_excel_file_loc,graph_select,"bolt")
        df_hybrid=arranjar(hybrid_excel_file_loc,graph_select,"hybrid")
        df_adhesive=arranjar(adhesive_excel_file_loc,graph_select,"adhesive")
        
        fig = go.Figure()
        
        df_global = pd.concat([df_bolt[['S_d_bolt', 'S_f_bolt']].copy(), df_hybrid[['S_d_hybrid', 'S_f_hybrid']].copy(),df_adhesive[['S_d_adhesive', 'S_f_adhesive']].copy()], axis=1)
        
        with st.expander("DataFrame"):
            st.dataframe(df_global)
        
        for names in ['bolt','hybrid','adhesive']:
            fig.add_trace(go.Scatter(x=df_global['S_d_'+names], y=df_global['S_f_'+names],
                          mode='lines',name=names))
        fig.update_layout(title='SLS Results',
                   xaxis_title='Displacement (mm)',
                   yaxis_title='Load (N)',template="seaborn")
        st.plotly_chart(fig)
        
       
        col1, col2, col3 = st.columns(3)
        
        col1.subheader("Bolt")
        col1.metric("Max Load (N)", round(df_global['S_f_bolt'].max(), 2))
        col1.metric("Max Displacement (mm)", round(df_global['S_d_bolt'].max(), 2))
        col1.metric("Lap Shear Strength (MPa)", round(df_global['S_f_bolt'].max()/area, 2))
        
        col2.subheader("Hybrid")
        col2.metric("Max Load (N)",round(df_global['S_f_hybrid'].max(), 2))
        col2.metric("Max Displacement (mm)",round(df_global['S_d_hybrid'].max(), 2))
        col2.metric("Lap Shear Strength (MPa)", round(df_global['S_f_hybrid'].max()/area, 2))
        
        col3.subheader("Adhesive")
        col3.metric("Max Load (N)",round(df_global['S_f_adhesive'].max(), 2))
        col3.metric("Max Displacement (mm)",round(df_global['S_d_adhesive'].max(), 2))
        col3.metric("Lap Shear Strength (MPa)", round(df_global['S_f_adhesive'].max()/area, 2))
        
    else:
        df_aux=pd.read_excel(excel_file_loc,sheet_name=graph_select,header=0,names=["S1_d","S1_f","S2_d","S2_f","S3_d","S3_f","S4_d","S4_f","S5_d","S5_f"])

        df_chosen=df_aux.dropna()
        with st.expander("DataFrame"):
            st.dataframe(df_chosen)
        avg_max_load=(df_chosen["S1_f"].max()+df_chosen["S2_f"].max()+df_chosen["S3_f"].max()+df_chosen["S4_f"].max()+df_chosen["S5_f"].max())/5
        avg_max_disp=(df_chosen["S1_d"].max()+df_chosen["S2_d"].max()+df_chosen["S3_d"].max()+df_chosen["S4_d"].max()+df_chosen["S5_d"].max())/5
        avg_lap_shear=(df_chosen["S1_f"].max()+df_chosen["S2_f"].max()+df_chosen["S3_f"].max()+df_chosen["S4_f"].max()+df_chosen["S5_f"].max())/(5*area)
        fig = go.Figure()

        for i in range (1,6):
            col_name_d = "S"+str(i)+"_d"
            col_name_f = "S"+str(i)+"_f"
            fig.add_trace(go.Scatter(x=df_chosen[col_name_d], y=df_chosen[col_name_f],
                          mode='lines',name="S"+str(i)))
        fig.update_layout(title='SLS Results',
                       xaxis_title='Displacement (mm)',
                       yaxis_title='Load (N)',template="seaborn")
        st.plotly_chart(fig)

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Max Load (N)", round(avg_max_load, 2))
        col2.metric("Average Max Displacement (mm)",round(avg_max_disp, 2))
        col3.metric("Average Lap Shear Strength (MPa)",round(avg_lap_shear, 2))
    
    
