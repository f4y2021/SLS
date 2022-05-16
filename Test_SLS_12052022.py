"""THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import openpyxl
from io import BytesIO
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

st.markdown("<h1 style='text-align: center; font-size:48px;font-weight:bold;'>SLS Connection Analysis</h1>", unsafe_allow_html=True)

with st.expander("Considered Configurations"):
    st.image('./data/considered_configurations.png')

#connection_tech = st.checkbox('I know the connection technology I want to use')

col11, col22 = st.columns(2)
with col11:
    first_choice = st.selectbox('Select Substrate #1',('C11', 'C12', 'C21', 'C22'))
with col22:
    second_choice = st.selectbox('Select Substrate #2',('C11', 'C12', 'C21', 'C22'))


connection_choice = st.selectbox('Select connection technology',('Bolt', 'Adhesive','Hybrid'))


excel_file_loc="./data/SLS_Results_"+connection_choice+".xlsx"
#first_choice = st.selectbox('Select Sample #1',('C11', 'C12', 'C21', 'C22'))
#second_choice = st.selectbox('Select Sample #2',('C11', 'C12', 'C21', 'C22'))
graph_select=first_choice+"_"+second_choice
st.write('You selected:', graph_select)
area=312.5
run_button=st.button("Run")

if run_button:

    df_aux=pd.read_excel(excel_file_loc,sheet_name=graph_select,header=0,names=["S1_d","S1_f","S2_d","S2_f","S3_d","S3_f","S4_d","S4_f","S5_d","S5_f"])

    df_chosen=df_aux.dropna()
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
    
    document = Document()

    document.add_heading('Document Title', 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='List Number'
    )
    
    document = io.BytesIO()
    
    st.download_button("Download Final Excel File",document,'demo.docx')
