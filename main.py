import streamlit as st
import pandas as pd
import folium
import copy
from streamlit_folium import st_folium
import branca
from math import comb as r
from math import degrees 
from math import atan

# Set page config
st.set_page_config(layout="wide")

# Set page title
APP_TITLE = """
Imām al-Bukhārī's Riḥla
"""
SUB_HEADER = """
Researched by Muntasir Zaman. 
Visit my blog at: https://hadithnotes.org/
"""
st.title(APP_TITLE)
st.subheader(SUB_HEADER)

show_popup = False
# LOCATIONS
locations = pd.read_csv('Data/locations.csv')
locations.set_index('location', inplace = True)


#Brazier Curve function
def bz(c,n=10,t=False):
    m,q,p,s=list(zip(*c)), len(c),[],(n-1 if t else n)/1.
    for i in range(n):
        b=[r(q-1,v)*(i/s)**v*(1-(i/s))**(q-1-v)for v in range(q)]
        p+=[(list(sum(j*k for j,k in zip(d,b))for d in m))]
    return p


# Intialize Map
#m = folium.Map(location=[29.31, 47.41], zoom_start=5, tiles='Stadia.StamenWatercolor', attr='&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://www.stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Madina logo by Quda designs')
m = folium.Map(location=[29.31, 47.41], zoom_start=5, tiles='Stadia.StamenWatercolor', attr='&')


# Decalre feature groups
feature_group_loc_names = folium.FeatureGroup(name='Display Names')
feature_group_loc_icons = folium.FeatureGroup(name='Display Icons')
fg_path_childhood = folium.FeatureGroup(name='Early Childhood')

# Add locations and text to the map
for index, loc in locations.iterrows():
    #Icon
    icon_path = loc['icon']
    icon = folium.CustomIcon(icon_path, icon_size=(loc['icon_l'], loc['icon_w']))

    #Popup
    popup_html = str(loc['popup_html'])
    iframe = branca.element.IFrame(html=popup_html , width=500, height=100)
    popup = folium.Popup(iframe, max_width=500)
    loc_icon = folium.Marker(
                location = [loc['lat'], loc['long']], 
                icon = icon,
                popup = popup
            )
    loc_icon.add_to(feature_group_loc_icons)

    # Add city names to the map

    html = '<div style="font-size: 10pt; color:black">' + index + '</div>'
    loc_name = folium.map.Marker(
                        [loc['lat'] , loc['long']],
                        icon=folium.DivIcon(
                            icon_size=(250,36),
                            icon_anchor=(-10,10),
                            html=html,
                            )
                        )
    
    loc_name.add_to(feature_group_loc_names)
    
# Function to add path to the map
def add_path(ft_group, startpoint, midpoint, endpoint, num_lines, line_color, line_wt, tooltip, arrow_color, arrow_size, arrow_dir_adjust=0):
    # Add path
    a = [locations.loc[startpoint]['lat'], locations.loc[startpoint]['long']]
    b = [locations.loc[endpoint]['lat'], locations.loc[endpoint]['long']]
    A_to_B = bz([a, *midpoint, b],
            n=num_lines, t=True)
    folium.PolyLine(
        locations=A_to_B,
        color=line_color,
        weight=line_wt,
        smooth_factor=0,
        tooltip=tooltip
    ).add_to(ft_group)

    # Add arrow on the path
    # Find slope
    mid_of_line = int(len(A_to_B)/2)
    slope = (A_to_B[mid_of_line][1]-A_to_B[mid_of_line-1][1]) / (A_to_B[mid_of_line][0]-A_to_B[mid_of_line-1][0])
    angle = degrees(atan(slope))
    folium.RegularPolygonMarker(location=A_to_B[mid_of_line],
                                fill_color=arrow_color,
                                color='black', #border color
                                opacity = 0, #border opacity
                                fillOpacity=1, 
                                number_of_sides=3, 
                                radius=arrow_size, 
                                rotation=180-angle-arrow_dir_adjust).add_to(fg_path_childhood)

# Bukahara to Merv  
add_path(ft_group=fg_path_childhood, startpoint='Bukhara', midpoint=[[39.28, 62.72]], endpoint='Merv', num_lines = 100, line_wt=2, line_color = '#187e18',
         tooltip = "Bukhara to Merv", arrow_size=6, arrow_color = '#000000'
         )

# Merv To Balkh
add_path(ft_group=fg_path_childhood, startpoint='Merv', midpoint=[[36.71, 63.14],[38.00, 65.85]], endpoint='Balkh', num_lines = 150, line_wt=2, line_color = '#187e18',
         tooltip = "Merv to Balkh", arrow_size=6, arrow_color = '#000000', arrow_dir_adjust=90
         )

# Balkh To Herat
add_path(ft_group=fg_path_childhood, startpoint='Balkh', midpoint=[[34.63, 66.45]], endpoint='Herat', num_lines = 100, line_wt=2, line_color = '#187e18',
         tooltip = "Balkh to Herat", arrow_size=6, arrow_color = '#000000', arrow_dir_adjust=90
         )

# Herat to Nishapur
add_path(ft_group=fg_path_childhood, startpoint='Herat', midpoint=[[34.84, 59.18]], endpoint='Nishapur', num_lines = 100, line_wt=2, line_color = '#187e18',
         tooltip = "Herat to Nishapur", arrow_size=6, arrow_color = '#000000', arrow_dir_adjust=-90
         )




"""
# Bukhara to Merv
A_to_B = bz([
                [locations.loc['Bukhara']['lat'], locations.loc['Bukhara']['long']],
                [39.52, 62.68],
                [locations.loc['Merv']['lat'], locations.loc['Merv']['long']]
            ],
            n=100, t=True)
folium.PolyLine(
    locations=A_to_B,
    color='#40514E',
    weight=1,
    smooth_factor=0,
    tooltip="Bukhara to Merv"
).add_to(fg_path_childhood)

# Find slope
mid_of_line = int(len(A_to_B)/2)
slope = (A_to_B[mid_of_line][1]-A_to_B[mid_of_line-1][1]) / (A_to_B[mid_of_line][0]-A_to_B[mid_of_line-1][0])
angle = degrees(atan(slope))
folium.RegularPolygonMarker(location=A_to_B[mid_of_line],
                            fill_color='black',
                            color='black', #border color
                            opacity = 0, #border opacity
                            fillOpacity=1, 
                            number_of_sides=3, 
                            radius=5, 
                            rotation=180-angle).add_to(fg_path_childhood)
    
"""

 
feature_group_loc_names.add_to(m)
feature_group_loc_icons.add_to(m)
fg_path_childhood.add_to(m)
folium.LayerControl().add_to(m)


st.write(locations)
st.write(locations.loc['Bukhara'])
st_data = st_folium(m, width=1600) 


