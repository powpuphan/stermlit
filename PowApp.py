import streamlit as st
import pandas as pd
import numpy as np
import folium as fo
from streamlit_folium import folium_static
import geopandas as gp

st.title('Streamlit with Folium')

"""
## An easy way to create a website using Python
"""

df1 = pd.read_csv('https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv')
df2 = pd.read_csv('https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv')
df3 = pd.read_csv('https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv')
df4 = pd.read_csv('https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv')
df5 = pd.read_csv('https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv')

df1 = df1[['latstartl', 'lonstartl', 'timestart']]
df2 = df2[['latstartl', 'lonstartl', 'timestart']]
df3 = df3[['latstartl', 'lonstartl', 'timestart']]
df4 = df4[['latstartl', 'lonstartl', 'timestart']]
df5 = df5[['latstartl', 'lonstartl', 'timestart']]

frames = [df1, df2, df3, df4, df5]

df = pd.concat(frames)

np.random.seed(10)
remove_n = 200000
drop_indices = np.random.choice(df.index, remove_n, replace=False)
df_subset = df.drop(drop_indices)
df = df_subset

st.write(df)


crs = "EPSG:4326"
geometry = gp.points_from_xy(df.lonstartl ,df.latstartl)
geo_df  = gp.GeoDataFrame(df,crs=crs,geometry=geometry)

nan_boundary  = gp.read_file('https://github.com/Maplub/AirQualityData/blob/master/nan_shp_wgs84.zip?raw=true')
nanall = nan_boundary.unary_union

nan_sta = geo_df.loc[geo_df.geometry.within(nanall)]


longitude = 100.819200
latitude = 19.331900

station_map = fo.Map(
	location = [latitude, longitude], 
	zoom_start = 10)

latitudes = list(nan_sta.latstartl)
longitudes = list(nan_sta.lonstartl)
labels = list(nan_sta.name)

for lat, lng, label in zip(latitudes, longitudes, labels):
	fo.Marker(
		location = [lat, lng], 
		popup = label,
		icon = fo.Icon(color='red', icon='heart')
	).add_to(station_map)

folium_static(station_map)
