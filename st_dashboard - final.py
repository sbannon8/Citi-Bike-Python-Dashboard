######################## DIVVY BIKES DASHABOARD ################################

# Import Libraries

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image 

### Initial Setting ####################

# set page and title
st.set_page_config(page_title = 'Divvy Bikes Strategy Dashboard', layout='wide')
st.title("Divvy Bikes Strategy Dashboard")

# create side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.radio('Select an aspect of the analysis',
  ["Intro page","Weather versus bike usage",
   "Most popular stations",
   "Map of bike trips", "Recommendations"])

### Import data  ########################

# main
df = pd.read_csv('reduced_data_sample.csv', index_col = 0)
# top 20 stations
top20 = pd.read_csv('top20.csv', index_col = 0)
# trips and temp aggregated by day
daily_df = pd.read_csv('dailyReport.csv', index_col = 0)

######################## PAGES #################################################

### PAGE: Intro ################# -----------------------------------------------

if page == "Intro page":
    # descriptive text
    st.markdown("#### This dashboard aims to provide helpful insights on the expansion problems Divvy Bikes currently faces.")
    st.markdown("Right now, Divvy bikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Most popular stations")
    st.markdown("- Weather versus bike usage")
    st.markdown("- Map of bike trips")
    st.markdown("- Recommendations")
    st.markdown("The dropdown menu on the left 'Aspect Selector' will take you to the different aspects of the analysis looked at.")

    # bike image
    myImage = Image.open("Divvy_Bike.jpg") #source: https://ride.divvybikes.com/blog
    st.image(myImage, width=550) 

### PAGE: Weather and bike usage ####### -----------------------------------------

elif page == 'Weather versus bike usage':

    # dual axis line chart of daily wheather vs trips
    fig_2 = make_subplots(specs = [[{"secondary_y": True}]])
    # trip usage
    fig_2.add_trace(
    go.Scatter(x = daily_df['date'], y = daily_df['ride_id'], name = 'Daily bike rides', marker={'color': daily_df['ride_id'],'color': 'blue'}),
    secondary_y = False
    )
    # weather
    fig_2.add_trace(
    go.Scatter(x=daily_df['date'], y = daily_df['avgTemp'], name = 'Daily temperature', marker={'color': daily_df['avgTemp'],'color': 'red'}),
    secondary_y=True
    )
    # chart layout
    fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022 New York',
    height = 500
    )
    st.plotly_chart(fig_2, use_container_width=True)

    # chart commentary
    st.markdown("There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from June to October.")

### PAGE: Most popular stations ####### -----------------------------------------

elif page == 'Most popular stations':

    # create season filter on the sidebar
    with st.sidebar:
        season_filter = st.multiselect(label= 'Select the season', options=df['season'].unique(),
    default=df['season'].unique())

    df1 = df.query('season == @season_filter')

    # show total rides KPI
    #total_rides = float(df1['bike_rides_daily'].count())  
    total_rides = float(df1.shape[0])
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))

    # Top 20 stations bar chart ---
    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')
    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value']))

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker={'color':top20['value'],'colorscale': 'Blues'}))
    fig.update_layout(
    title = 'Top 20 most popular bike stations in 2022 New York',
    xaxis_title = 'Start stations',
    yaxis_title ='Sum of trips',
    width = 800, height = 500
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("There are some start stations that are more popular than others, with the top 3 being W 21 St & 6 Ave, West S & Chamber St as well as Broadway & W 58 St. There is a jump between the highest and lowest bars of the plot of about 3.5k, indicating preferences for the leading stations. The season filter, located in the sidebar, can be used to view popularity changes by season - there are some changes to the order of the overall top 3 as well as the introduction of stations such as 1 Ave & E 68 St and various Broadway intersections. Station popuarity an be explored more through the bike trips map accessed through the Aspect Selector.")

### PAGE: Routes map ############## ------------------------------------------

elif page == 'Map of bike trips': 

    # map
    st.write("Map showing top 3 trips in New York")
    path_to_html = "top3 trips map.html"

    with open(path_to_html,'r') as f: 
        html_data = f.read()

    st.components.v1.html(html_data,height=500)

    # map commentary
    st.markdown("The top 3 routes (marked by a yellow dot on the map) are:")
    st.markdown("7 Ave & Central Park, Central Park S & 6 Ave, and Roosevelt Island Trammway.  The top 3 routes consist of over 8,000 trips and are located along Central Park or the Roosevelt Island Tramway- an aerial tramway providing a scenic experience and easy access to local attractions.")
    st.markdown("As a reminder, the top 3 start stations were: W 21 St & 6 Ave, West S & Chamber St, and Broadway & W 58 St. With the map of aggregated trips, we can see that even though these are popular start stations, they don't necessarily account for the most commonly taken trips")

    st.markdown("### **From Chaos to Core: Filtering NYC Bike Routes by Usage**")
    st.markdown("This video shows the same map above, starting with a visualization of all routes and is then filtered down by number of times taken. It displays that as popularity increases, centrality to New York City increases, particularly towards popular attractions.")

    video_path = "MapDemo.mp4"
    
    # Open video in binary mode
    with open(video_path, 'rb') as video_file:
        video_bytes = video_file.read()
    
    # Display video
    st.video(video_bytes)

### PAGE: Recommendations ########## -------------------------------------------

else:
    
    st.header("Conclusions and recommendations")
    #bikes = Image.open("recs_page.png")  #source: Midjourney
    #st.image(bikes)
    st.markdown("### Our analysis has shown that Divvy Bikes should focus on the following objectives moving forward:")
    st.markdown("- Add more stations throughout Manhattan where popular tourist attrractions are concentrated, focusing on areas with higher bike-friendly paths and centrality to multiple attractions. Central Park and surrounding areas as well as lower Manhattan have the most demand.")
    st.markdown("- Ensure that bikes are fully stocked in all these stations during the warmer months in order to meet the higher demand, but provide a lower supply in winter and late autumn to reduce logistics costs")
                                                                                   