import streamlit as st
from pyecharts.charts import Bar
from streamlit_echarts import st_echarts, st_pyecharts
from pyecharts.charts import EffectScatter
from pyecharts.globals import SymbolType
from pyecharts import options as opts

from pyecharts.charts import Map

#create dataset for the chart, v1 is the revenue of Shopify in million dollars, x is the year

def main():
    st.sidebar.title("PYECHART")
    action = st.sidebar.selectbox("Navigation", ["Scatter","Map"])
    if action == "Scatter":
        st.title("Scatter")
        # import libraries

        v1 = [24,50,105,205,389,673,1073,1578]
        v2 = [3,5,8,12,16,23,40,56,72]
        x = ["2012", "2013", "2014", "2015", "2016", "2017","2018","2019"]

        c = (
        EffectScatter()
        .add_xaxis(x)
        .add_yaxis("Shopify", v1,is_selected = True,symbol_size = 20, symbol=SymbolType.DIAMOND)
        .add_yaxis("Alibaba", v2,is_selected = True,symbol_size = 20)
        )
        #c.render_notebook()
        st_pyecharts(c)
    elif action == "Map":
        st.title("Map")
        
        #value =[155, 10, 66, 78, 33, 80, 190, 53, 49.6]
        #attr = [ "Fujian", "Shandong", "Beijing", "Shanghai", "Gansu", "Xinjiang", "Henan", "Guangxi", "Tibet"]

        value = [155, 10, 66, 78, 33, 80, 190, 53, 49.6]
        attr = ["福建", "山东", "北京", "上海", "甘肃", "新疆", "河南", "广西", "西藏"]
        
        list1 = [[attr[i],value[i]] for i in range(len(attr))]

        map = Map(init_opts=opts.InitOpts(width="1000px", height="460px"))

        map.add("Total Confirmed Cases", list1, maptype="china") #add world map
        #map_1.set_global_opts( #set global configurations
        # visualmap_opts=opts.VisualMapOpts(max_=1100000,    is_piecewise=False),
        # legend_opts=opts.LegendOpts(is_show=False), #show legend or not
        # )
        #map.render_notebook()
        st_pyecharts(map)
    

if __name__ == "__main__":
    main()