import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium import Choropleth, Circle, Marker

#create dataset for the chart, v1 is the revenue of Shopify in million dollars, x is the year

def main():
    st.sidebar.title("GeoSpatial Analysis")
    action = st.sidebar.selectbox("Navigation", ["PLOTLY","FOLIUM"])
    if action == "PLOTLY":
        st.title("Plotly")
        fp = st.sidebar.file_uploader("Select your file") 
        st.sidebar.button("cek")

    elif action == "FOLIUM":
        st.title("Folium")
        df = pd.read_excel('lokasitps.xlsx', sheet_name='teamtouring.net', engine='openpyxl')
        tps = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['longitude'], df['latitude']))
        tps.crs = {'init': 'epsg:4326'}
        map = plotting_point(tps, 'latitude', 'longitude')
        folium_static(map)



def plotting_point(data, lat_name, long_name, type_map='openstreetmap', center_loc_lat = 0, center_loc_long = 0):
    if (center_loc_lat == 0 or center_loc_long == 0):
        center_loc_lat = data.loc[0,lat_name]
        center_loc_long = data.loc[0,long_name]

    map = folium.Map(location=[center_loc_lat,center_loc_long], tiles=type_map, zoom_start=10)

    for idx, row in data.iterrows():
        Marker([row[lat_name], row[long_name]]).add_to(map)
    
    return map
    

if __name__ == "__main__":
    main()