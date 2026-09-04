import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Map Test",
    layout="wide"
)

st.title("🗺️ NER-SMART Map Test")

m = folium.Map(
    location=[26.1445, 91.7362],
    zoom_start=10
)

folium.Marker(
    [26.1445, 91.7362],
    popup="Guwahati"
).add_to(m)

st_folium(
    m,
    width=1000,
    height=600
)