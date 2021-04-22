import streamlit as st
import geopandas as gpd
import folium
import pandas as pd
from streamlit_folium import folium_static
from folium import Choropleth, Circle, Marker
import os

from libraries.plotly_lib import plot_scatter, plot_line, plot_bubble_map, plot_density, plot_choropleth
from libraries.indo_geo import Indo_Geo

def main():
    st.sidebar.title("GeoSpatial Analysis")
    action = st.sidebar.selectbox("Navigation", ["PLOTLY","FOLIUM"])
    if action == "PLOTLY":
        st.title("Plotly")
        type_map = st.sidebar.selectbox("type",["Choropleth","Scatter","Line","Bubblemap","Density"])
        
        if (type_map == "Choropleth"):
            location = st.sidebar.text_input("location")
            fp = st.sidebar.file_uploader("Select your file") 
            df = load_table(fp)
            st.write(df)
            column_compare = st.sidebar.text_input("Column name for compare")
            column_value = st.sidebar.text_input("Column name for value")

            if st.sidebar.button("Plot"):
                dataGeo = Indo_Geo(location)
                fig =   plot_choropleth(df, dataGeo.df_location, dataGeo.region, column_compare, column_value)
                #st.write(fig[1])
                st.plotly_chart(fig[0])

        elif (type_map == "Scatter"):
            location = st.sidebar.text_input("location")
            fp = st.sidebar.file_uploader("Select your file") 
            df = load_table(fp)
            st.write(df)
            hover_name = st.sidebar.text_input("hover name")
            longitude = st.sidebar.text_input("Column name for longitude")
            latitude = st.sidebar.text_input("Column name for latitude")

            if st.sidebar.button("Plot"):
                dataGeo = Indo_Geo(location)
                fig =   plot_scatter(df, dataGeo.df_location, location.upper(), longitude, latitude, hover_name)
                st.plotly_chart(fig)

        elif (type_map == "Line"):
            location = st.sidebar.text_input("location")
            fp = st.sidebar.file_uploader("Select your file") 
            df = load_table(fp)
            st.write(df)
            longitude = st.sidebar.text_input("Column name for longitude")
            latitude = st.sidebar.text_input("Column name for latitude")
            style_map = st.sidebar.selectbox("map style",["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner","stamen-watercolor"])
            
            if st.sidebar.button("Plot"):
                dataGeo = Indo_Geo(location)
                center_coordinate = dataGeo.get_median_coordinate()
                fig = plot_line(df, latitude, longitude, location.upper(), style_map, center_coordinate)
                st.plotly_chart(fig)

        elif(type_map=="Bubblemap"):
            location = st.sidebar.text_input("location")
            fp = st.sidebar.file_uploader("Select your file") 
            df = load_table(fp)
            df['size'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
            st.write(df)
            hover_name = st.sidebar.text_input("hover name")
            longitude = st.sidebar.text_input("Column name for longitude")
            latitude = st.sidebar.text_input("Column name for latitude")
            size = st.sidebar.text_input("Column name for size bubble")
            if st.sidebar.button("Plot"):
                dataGeo = Indo_Geo(location)
                fig =   plot_bubble_map(df, location.upper(), longitude, latitude, hover_name, size)
                st.plotly_chart(fig)

        elif (type_map == "Density"):
            location = st.sidebar.text_input("location")
            fp = st.sidebar.file_uploader("Select your file") 
            df = load_table(fp)
            df['size'] = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
            st.write(df)
        
            longitude = st.sidebar.text_input("Column name for longitude")
            latitude = st.sidebar.text_input("Column name for latitude")
            size = st.sidebar.text_input("Column name for magnitude")
            radius = st.sidebar.text_input("Radius")
            style_map = st.sidebar.selectbox("map style",["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner","stamen-watercolor"])
            
            if st.sidebar.button("Plot"):
                dataGeo = Indo_Geo(location)
                center_coordinate = dataGeo.get_median_coordinate()
                fig = plot_density(df, latitude, longitude, location.upper(),size, int(radius), style_map,center_coordinate)
                st.plotly_chart(fig)


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

def load_table(data):
    df = pd.read_excel('lokasitps.xlsx', sheet_name='Lembar1', engine='openpyxl')
    return df

def add(a,b):

        c = a+b

        return c
    

if __name__ == "__main__":
    main()