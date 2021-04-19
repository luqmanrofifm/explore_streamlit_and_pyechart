import geopandas as gpd
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go
import numpy as np

def plot_scatter(data,location, name_long, name_lat, name_hover):
    map = convert_shp_to_geojson(province = location)
    with open('fileJSON//coba_jogja.json') as f:
        map_gejson = json.load(f)

    fig = px.choropleth(map,
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

def convert_shp_to_geojson(province = ""):
    ind = gpd.read_file("SHP//Indo_Kab_Kot.shp")
    ind =  preprocessing_shp(ind)
    map = ind[ind["PROVINSI"] == "DAERAH ISTIMEWA YOGYAKARTA"]
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


    