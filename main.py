import streamlit as st
import folium
from streamlit_folium import st_folium

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

# LOCATIONS
KABA = [21.42255297077458, 39.82618611908724]
BUKHARA = [39.7681, 64.4556]
BAGHDAD = [33.2622, 44.2470]

# CUSTOM ICONS
kaba_image = 'Icons/kaaba.png'
kaba_icon = folium.CustomIcon(
    kaba_image,
    icon_size=(20,20)
)

red_star = 'Icons/red-star.png'
red_star_icon = folium.CustomIcon(
    red_star,
    icon_size=(20,20)
)

black_dot = 'Icons/black-dot.png'
black_dot_icon = folium.CustomIcon(
    black_dot,
    icon_size=(40,40)
)

# Intialize Map
m = folium.Map(location=[29.31, 47.41], zoom_start=5, tiles='Cartodb Positron')


# Add locations and text to the map

# 1. Makkah
folium.Marker(
    location = KABA, 
    icon = kaba_icon,
    popup = 'Makkah'
).add_to(m)

div_html ="""
<div style="font-family: Brill, sans-serif; font-size: 8pt; text-align: left; color: black">
    Visited in 210 AH.
</div>

"""
#2. Bukahara
folium.Marker(
    location = BUKHARA , 
    icon = red_star_icon,
    popup = 'Bukhara'
).add_to(m)

#3. Baghdad
folium.Marker(
    location = BAGHDAD, 
    icon = black_dot_icon,
    popup = 'Baghdad'
).add_to(m)


# Add Polylines
BUKHARA_to_BAGHDAD=[
    BUKHARA,
    [38.365943567086376, 63.34372099695885],
    [35.68524911544845, 58.418099097917136],
    [34.111382700828514, 52.724847812011774],
    [33.36665999541276, 46.87167373717649],
    BAGHDAD
]

BAGHDAD_to_MAKKAH=[
    BAGHDAD,
    [30.729891948661574, 44.51756526465571],
    [28.272300302456024, 43.87206833165582],
    [25.92612917935021, 43.19967569311427],
    [23.999993378286593, 42.12384747144779],
    [21.994725443763087, 40.429418022323084],
    KABA
]

# Bukhara to Baghdad
folium.PolyLine(
    locations=BUKHARA_to_BAGHDAD,
    color='#000000',
    weight=2,
    smooth_factor=1,
    tooltip="Bukhara to Baghdad"
).add_to(m)
folium.RegularPolygonMarker(location=BUKHARA_to_BAGHDAD[3],
                            fill_color='black',
                            color='black', #border color
                            opacity = 0, #border opacity
                            fillOpacity=1, 
                            number_of_sides=3, 
                            radius=9, 
                            rotation=160).add_to(m)

#Baghdad To Makkah
folium.PolyLine(
    locations=BAGHDAD_to_MAKKAH,
    color='#000000',
    weight=2,
    smooth_factor=1,
    tooltip="Baghdad to Makkah"
).add_to(m)
folium.RegularPolygonMarker(location=BAGHDAD_to_MAKKAH[3],
                            fill_color='black',
                            color='black', #border color
                            opacity = 0, #border opacity
                            fillOpacity=1, 
                            number_of_sides=3, 
                            radius=9, 
                            rotation=97).add_to(m)

st_data = st_folium(m, width=1400)


