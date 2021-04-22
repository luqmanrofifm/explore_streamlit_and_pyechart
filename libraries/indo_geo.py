import pandas as pd
import geopandas as gpd


class Indo_Geo:
    def __init__(self, location):
        self.location = location.upper()
        Indo_Geo.collect_data_location(self)
        Indo_Geo.get_specific_location(self)

    
    def get_specific_location(self):
        if (self.location in self.list_province):
            self.region = "PROVINSI"
            self.df_location = self.all_data_geo[self.all_data_geo["PROVINSI"] == self.location]
        elif (self.location in self.list_city):
            self.region = "KABKOT"
            self.df_location = self.all_data_geo[self.all_data_geo["KABKOT"] == self.location]
            
    def get_median_coordinate(self):
        self.df_location['Center_point'] = self.df_location['geometry'].centroid

        self.df_location["lat"] = self.df_location.Center_point.map(lambda p: p.x)
        self.df_location["long"] = self.df_location.Center_point.map(lambda p: p.y)

        return self.df_location["long"].median(), self.df_location["lat"].median()

    def collect_data_location(self):
        ind = gpd.read_file("SHP//Indo_Kab_Kot.shp")
        ind =  Indo_Geo.preprocessing_shp(ind)
        self.all_data_geo = ind
        self.list_province = list(set(ind.PROVINSI))
        self.list_city = list(set(ind.KABKOT))
    
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
