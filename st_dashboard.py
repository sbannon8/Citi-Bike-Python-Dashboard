######################## DIVVY BIKES DASHABOARD ################################
import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt 

######################## Initial settings for dashboard  ########################
st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")
st.markdown("The dashboard will help with the expansion problems Divvy currently faces")
st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.")

######################## Import data  ###########################################
df = pd.read_csv('reduced_data.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)
daily_df = pd.read_csv('dailyReport.csv', index_col = 0)

######################## Define charts ###########################################

## Top 20 Stations ----------------
# bar chart

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['count'], marker = {'color' : top20['count'], 'colorscale' : 'Blues'}))
fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in New York',
    xaxis_title = 'Start Stations', 
    yaxis_title = 'Sum of Trips', 
    width = 900, height = 600
)
st.plotly_chart(fig, use_container_width = True)

## Daily Trips vs Avg Temp ----------
## line chart 

fig_2 = make_subplots(specs = [[{"secondary_y": True}]])

fig_2.add_trace(
go.Scatter(x = daily_df['date'], y = daily_df['ride_id'], name = 'Daily bike rides', marker={'color': daily_df['ride_id'],'color': 'blue'}),
secondary_y = False
)

fig_2.add_trace(
go.Scatter(x=daily_df['date'], y = daily_df['avgTemp'], name = 'Daily temperature', marker={'color': daily_df['avgTemp'],'color': 'red'}),
secondary_y=True
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022 New York',
    height = 600
)

st.plotly_chart(fig_2, use_container_width=True)

######################## Map ###############################################
path_to_html = r"C:\Users\steve\Downloads\kepler.gl.html"

# Read file and keep in variable
with open(path_to_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height=1000)
                                                                                   