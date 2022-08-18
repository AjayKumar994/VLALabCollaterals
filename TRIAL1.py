from calendar import c
from email.policy import default
from itertools import count, groupby
from msilib import add_data
from msilib.schema import Class, tables
import os
import os.path
from os import path
import string
import sys
from turtle import color
from typing import Iterable
import pandas as pd
pd.set_option('display.max_rows', None)
import datetime
import time
import mysql.connector
import numpy as np
import plotly.express as px
import streamlit as st
from openpyxl import workbook
import altair as alt
from vega_datasets import data
from natsort import natsorted



config = {
    'user' : 'alot_user',
    'password' : 'Alotuser1234',
    'host' : 'maria3083-lb-pg-in.dbaas.intel.com',
    'port' : 3307,
    'database' : 'alot_db'
}
cnx = mysql.connector.connect(**config)
full_asset = pd.read_sql_query("SELECT * FROM full_asset_mys", cnx)
cnx.close()

asset_class = []
for x in range (len(full_asset["Class"])):
    asset_class.append(full_asset["Class"][x])
    
asset_class = list(filter(None, asset_class)) ## filter empty value
asset_class = list(dict.fromkeys(asset_class)) ## remove duplicate
asset_class = natsorted(asset_class) ## sort by ascending order

asset_status = []
for x in range (len(full_asset["Status(hardware_status)"])):
    asset_status.append(full_asset["Status(hardware_status)"][x])

asset_status = list(filter(None, asset_status)) ## filter empty value
asset_status = list(dict.fromkeys(asset_status)) ## remove duplicate
asset_status = natsorted(asset_status) ## sort by ascending order

st.set_page_config(page_title="Lab Collaterals Dashboard")
st.title('Intel Inventory Dashboard')
st.subheader('Enter data')

uploaded_file=st.file_uploader('Choose a XLSX file',type='xlsx')
if uploaded_file:
    st.markdown('---')
    df=pd.read_excel(uploaded_file,engine='openpyxl')
    st.dataframe(df)

#-------------------------------------------------------------------------------------------
#----Mainpage
#----Allow user to select analysis

#learn function from melvin to simplify repeative code
#col_1= full_asset.columns.get_loc('Class')
#col_2= full_asset.columns.get_loc('Barcode')
#col_3=full_asset.columns.get_loc('Serial Number')
##col_4=full_asset.columns.get_loc('Model')
#col_5=full_asset.columns.get_loc('Status(hardware_status)')
#col_6=full_asset.columns.get_loc('Substatus')

#declare as list
#col=[]
#col.append(col_1)
#col.append(col_2)
#col.append(col_3)
##col.append(col_4)
#col.append(col_5)
#col.append(col_6)

#genereate output of the filtered columns
#df =full_asset[full_asset.columns[col]]
df =full_asset[["Class", "Status(hardware_status)", "Substatus"]]


st.columns([3, 1])
groupby_column=st.selectbox(
    'What you want to look into?',
    asset_class
)

#generate pivot
table = pd.pivot_table(data=df,index=['Status(hardware_status)'],columns=['Class'],
                       values ='Substatus',aggfunc='count',fill_value=0)
st.table(table[groupby_column])

#Group dataframe
#output= (asset_status)
#df_grouped = df.groupby(by=[groupby_column])[output].count()
#st.dataframe(df_grouped)

#plot chart
fig1 =px.bar(
    table[groupby_column],
    x=asset_status,
    y=groupby_column,
    opacity = 0.9,
    color=asset_status
    #orientation="v",
    #barmode='relative',
)

st.plotly_chart (fig1)
