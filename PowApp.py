import streamlit as st
import pandas as pd
import numpy as np
#import folium as fo
#from streamlit_folium import folium_static
#import geopandas as gp
import pydeck as pdk
import altair as alt


st.title('''
Streamlit with Folium By Puphan Pornsilkiat 6030819321
''')

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
remove_n = 20000
drop_indices = np.random.choice(df.index, remove_n, replace=False)
df_subset = df.drop(drop_indices)
df = df_subset
df['timestart']  = pd.to_datetime(df['timestart'])


data = df

DATE_TIME = "timestart"

hour = st.slider("Hour to look at", 0, 23)

data = data[data[DATE_TIME].dt.hour == hour]

st.subheader("Geo data between %i:00 and %i:00" % (hour, (hour + 1) % 24))

st.write("""
# Map
""")

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/streets-v9',
     initial_view_state=pdk.ViewState(
        latitude=13.687455,
         longitude=100.536915,
         zoom=9,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=data,
            get_position='[lonstartl, latstartl]',
            auto_highlight=True,
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=data,
             get_position='[lonstartl, latstartl]',
             get_color='[200, 30, 200, 160]',
             get_radius=200,
         ),
     ],
 ))


st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour + 1))
]
hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "pickups": hist})

st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ), use_container_width=True)

if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
