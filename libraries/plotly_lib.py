import geopandas as gpd
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go
import numpy as np
from fuzzywuzzy import fuzz

def plot_choropleth(data, df_geo, location, column_compare, column_value):
    geo_copy = df_geo.copy()
    geo_copy.reset_index(drop=True, inplace=True)

    for id,i in enumerate(data[column_compare]):
        list_result = []
        for j in geo_copy["KABKOT"]:
            ratio = fuzz.token_sort_ratio(i, j)
            list_result.append(ratio)
        index = list_result.index(max(list_result))
        
        geo_copy.at[index,column_value] =  data[column_value].loc[id]
    
    print(geo_copy)
    
    geo_copy.to_file("fileJSON//cobaJogja.json", driver="GeoJSON")

    with open('fileJSON//cobaJogja.json') as f:
        json_val = json.load(f)

    fig = px.choropleth(geo_copy,
                    geojson=json_val,
                    locations="KABKOT",
                    color = column_value,
                featureidkey="properties.KABKOT")
                
    fig.update_geos(fitbounds="locations", visible=False)

    return fig,geo_copy

def plot_scatter(data, df_geo, location, name_long, name_lat, name_hover):
    #map = convert_shp_to_geojson(province = location, status = True)
    df_geo.to_file("fileJSON//coba_jogja.json", driver="GeoJSON")

    with open('fileJSON//coba_jogja.json') as f:
        map_gejson = json.load(f)

    fig = px.choropleth(df_geo,
                    geojson=map_gejson,
                    locations="KABKOT",
                featureidkey="properties.KABKOT")

    fig2 = px.scatter_geo(data,
                        lat=data[name_lat],
                        lon=data[name_long],
                        hover_name=name_hover)

    fig2.update_traces( marker=dict(color="Black",
                                    size=5,
                                    line=dict(width=2,
                                            color='Black')),
                                    selector=dict(mode='markers'))

    fig.add_trace(
        fig2.data[0]
    )
                        
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

def plot_line(data, name_lat, name_long, location, style_map, center_coordinate):
    fig = px.line_mapbox(data, lat=name_lat, lon=name_long, zoom=3, height=300)
    
    #df_loc = convert_shp_to_geojson(province = location)
    #df_loc['Center_point'] = df_loc['geometry'].centroid

    #df_loc["lat"] = df_loc.Center_point.map(lambda p: p.x)
    #df_loc["long"] = df_loc.Center_point.map(lambda p: p.y)

    fig.update_layout(mapbox_style=style_map, mapbox_zoom=9, mapbox_center_lat = center_coordinate[0],
        margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def plot_bubble_map(data, df_geo, location, name_long, name_lat, name_hover, size_column):
    map = convert_shp_to_geojson(province = location, status = True)
    with open('fileJSON//coba_jogja.json') as f:
        map_gejson = json.load(f)

    fig = px.choropleth(map,
                    geojson=map_gejson,
                    locations="KABKOT",
                featureidkey="properties.KABKOT")

    fig2 = px.scatter_geo(data,
                        lat=data[name_lat],
                        size = size_column,
                        lon=data[name_long],
                        hover_name=name_hover)

    fig2.update_traces( marker=dict(color="Black",
                                    line=dict(width=2,
                                            color='Black')),
                                    selector=dict(mode='markers'))

    fig.add_trace(
        fig2.data[0]
    )
                        
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

def plot_density(data, name_lat, name_long, location, size_column, size_radius, style_map, center_coordinate):
    '''
    df_loc = convert_shp_to_geojson(province = location)
    df_loc['Center_point'] = df_loc['geometry'].centroid

    df_loc["lat"] = df_loc.Center_point.map(lambda p: p.x)
    df_loc["long"] = df_loc.Center_point.map(lambda p: p.y)
    '''
    fig = px.density_mapbox(data, lat=name_lat, lon=name_long, z=size_column, radius=size_radius,
                        center=dict(lat=center_coordinate[0], lon=center_coordinate[1]), zoom=9,
                        mapbox_style=style_map)
    return fig


def convert_shp_to_geojson(province = "", status = False):
    ind = gpd.read_file("SHP//Indo_Kab_Kot.shp")
    ind =  preprocessing_shp(ind)
    map = ind[ind["PROVINSI"] == "DAERAH ISTIMEWA YOGYAKARTA"]
    if (status == True):
        map.to_file("fileJSON//coba_jogja.json", driver="GeoJSON")
    return map

def preprocessing_shp(data):
    list_duplicate = ['Sulawesi Tengah', 'Sumatera Barat', 'Sulawesi Tenggara', 'Nanggroe Aceh Darussalam']
    for i, val in enumerate(data['PROVINSI']):
        if (val in list_duplicate and val == 'Nanggroe Aceh Darussalam'):
            data.loc[i,'PROVINSI'] = 'ACEH'
            data.loc[i,'KABKOT'] = data.loc[i,'KABKOT'].upper()
        elif (val in list_duplicate and val != 'Nanggroe Aceh Darussalam'):
            data.loc[i,'PROVINSI'] = val.upper()
            data.loc[i,'KABKOT'] = data.loc[i,'KABKOT'].upper()
    
    data = data.sort_values(by = ['PROVINSI'])
    return data


    