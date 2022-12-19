import streamlit as st
import pydeck as pdk
import pandas as pd
import random as rd
import matplotlib.pyplot as plt

st.title("California Fire Data (2018 to 2020)")
df_cal = pd.read_csv("C:/Users/jake_/Documents/CS230/Maps/California_Fire_Incidents.csv")
df_cal.rename(columns={"Latitude":"lat", "Longitude": "lon"}, inplace=True) # Changes column names to allow Streamlit mapping


URL_List = ["https://commons.wikimedia.org/wiki/Category:Torches_in_logos#/media/File:Drepeau.png"]
sub_df1 = df_cal[(df_cal["lat"] > 32) & (df_cal["lat"] < 42) & (df_cal["lon"] < 0) & (df_cal["lon"] > -125)] # Filters out latitudes that do not exist, are 0, or do not make sense for the data set
sub_df_cal = sub_df1[["AcresBurned", "lat", "lon"]] # Taking only the columns needed for the first map
large_sub_df_list = sub_df_cal[sub_df_cal["AcresBurned"] >= 5000]
medium_sub_df_list = sub_df_cal[(sub_df_cal["AcresBurned"] >= 1000) & (sub_df_cal["AcresBurned"] < 5000)] # Filters dataset into three categories based on how many acres the fire burned
small_sub_df_list = sub_df_cal[(sub_df_cal["AcresBurned"] > 0.1) & (sub_df_cal["AcresBurned"] < 1000)]
sub_large = large_sub_df_list[["lat", "lon", "AcresBurned"]]
sub_medium = medium_sub_df_list[["lat", "lon", "AcresBurned"]] # Makes the sub_df_lists plottable
sub_small = small_sub_df_list[["lat", "lon", "AcresBurned"]]
selected_map = st.sidebar.selectbox(options=["Small (<1000 Acres Burned)", "Medium (>1000 and 5000< Acres Burned)", "Large (>5000 Acres Burned)"], label="Choose the size(s) of fire you want to display:")


if selected_map == "Small (<1000 Acres Burned)":
        st.title("Small Fires")
        view_small = pdk.ViewState(
        latitude=sub_small["lat"].mean(),
        longitude=sub_small["lon"].mean(),
        zoom=4.75,
        pitch=1)

        layer1 = pdk.Layer(type = 'ScatterplotLayer',
                      data=sub_small,
                      get_position='[lon, lat]',
                      get_radius=5000,
                      get_color=[0,0,255],
                      pickable=True
                      )
        tool_tip = {"html": "Acres Burned:<br/> <b>{AcresBurned}</b>",
                        "style": { "backgroundColor": "cyan",
                            "color": "black"}
                        }

        map = pdk.Deck(
                map_style='mapbox://styles/mapbox/satellite-streets-v12',
                initial_view_state=view_small,
                layers=[layer1],
                tooltip= tool_tip
        )

        st.pydeck_chart(map)
if selected_map == "Medium (>1000 and 5000< Acres Burned)":
        st.title("Medium Fires")
        view_medium = pdk.ViewState(
        latitude=sub_medium["lat"].mean(),
        longitude=sub_medium["lon"].mean(),
        zoom=4.75,
        pitch=1)

        layer1 = pdk.Layer(type = 'ScatterplotLayer',
                      data=sub_medium,
                      get_position='[lon, lat]',
                      get_radius=10000,
                      get_color=[0,0,255],
                      pickable=True
                      )

        layer2 = pdk.Layer('ScatterplotLayer',
                      data=sub_medium,
                      get_position='[lon, lat]',
                      get_radius=5000,
                      get_color=[255,0,255],
                      pickable=True
                      )

        tool_tip = {"html": "Acres Burned:<br/> <b>{AcresBurned}</b>",
                        "style": { "backgroundColor": "purple",
                            "color": "black"}
                        }

        map = pdk.Deck(
                map_style='mapbox://styles/mapbox/satellite-streets-v12',
                initial_view_state=view_medium,
                layers=[layer1, layer2],
                tooltip=tool_tip
        )

        st.pydeck_chart(map)
if selected_map == "Large (>5000 Acres Burned)":
        st.title("Large Fires")
        view_large = pdk.ViewState(
        latitude=sub_large["lat"].mean(),
        longitude=sub_large["lon"].mean(),
        zoom=4.75,
        pitch=1)

        layer1 = pdk.Layer(type = 'ScatterplotLayer',
                      data=sub_large,
                      get_position='[lon, lat]',
                      get_radius=15000,
                      get_color=[0,0,255],
                      pickable=True
                      )

        layer2 = pdk.Layer('ScatterplotLayer',
                      data=sub_large,
                      get_position='[lon, lat]',
                      get_radius=7500,
                      get_color=[255,0,255],
                      pickable=True
                      )

        layer3 = pdk.Layer('ScatterplotLayer',
                      data=sub_large,
                      get_position='[lon, lat]',
                      get_radius=3750,
                      get_color=[255,255,255],
                      pickable=True
                      )

        tool_tip = {"html": "Acres Burned:<br/> <b>{AcresBurned}</b>",
                        "style": { "backgroundColor": "purple",
                            "color": "black"}
                        }

        map = pdk.Deck(
                map_style='mapbox://styles/mapbox/satellite-streets-v12',
                initial_view_state=view_large,
                layers=[layer1, layer2, layer3],
                tooltip=tool_tip
        )

        st.pydeck_chart(map)

charttype = st.sidebar.selectbox("Please select a Chart Type:", ["Histogram", "Scatterplot"])
datatype = st.sidebar.selectbox("Please select data to display:", ["Structures Damaged", "Structures Destroyed"])

if charttype == "Histogram" and datatype == "Structures Damaged" and selected_map == "Small (<1000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Frequency of Structures Damaged by Fires")
    small_df_list = sub_df1[(sub_df1["AcresBurned"] > 0.1) & (sub_df1["AcresBurned"] < 1000)]
    sub_df3 = small_df_list[(small_df_list["StructuresDamaged"] > 0)]
    y = small_df_list[["StructuresDamaged"]].values.tolist() # Need to use .tolist() to make the series plottable
    ax.hist(y, stacked=True)
    plt.xlabel("Structures Damaged")
    plt.ylabel("Frequency")
    st.pyplot(fig)
if charttype == "Histogram" and datatype == "Structures Damaged" and selected_map == "Medium (>1000 and 5000< Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Frequency of Structures Damaged by Fires")
    medium_df_list = sub_df1[(sub_df1["AcresBurned"] >= 1000) & (sub_df1["AcresBurned"] < 5000)]
    sub_df3 = medium_df_list[(medium_df_list["StructuresDamaged"] > 0)]
    y = medium_df_list[["StructuresDamaged"]].values.tolist()
    ax.hist(y, stacked=True)
    plt.xlabel("Structures Damaged")
    plt.ylabel("Frequency")
    st.pyplot(fig)
if charttype == "Histogram" and datatype == "Structures Damaged" and selected_map == "Large (>5000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Frequency of Structures Damaged by Fires")
    large_df_list = sub_df1[sub_df1["AcresBurned"] >= 5000]
    sub_df3 = large_df_list[(large_df_list["StructuresDamaged"] > 0)]
    y = large_df_list[["StructuresDamaged"]].values.tolist()
    ax.hist(y, stacked=True)
    plt.xlabel("Structures Damaged")
    plt.ylabel("Frequency")
    st.pyplot(fig)

if charttype == "Histogram" and datatype == "Structures Destroyed" and selected_map == "Small (<1000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Frequency of Structures Destroyed by Fires")
    small_df_list = sub_df1[(sub_df1["AcresBurned"] > 0.1) & (sub_df1["AcresBurned"] < 1000)]
    sub_df3 = small_df_list[(small_df_list["StructuresDestroyed"] > 0)]
    y = small_df_list[["StructuresDestroyed"]].values.tolist()
    ax.hist(y, stacked=True)
    plt.xlabel("Structures Destroyed")
    plt.ylabel("Frequency")
    st.pyplot(fig)
if charttype == "Histogram" and datatype == "Structures Destroyed" and selected_map == "Medium (>1000 and 5000< Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Frequency of Structures Destroyed by Fires")
    medium_df_list = sub_df1[(sub_df1["AcresBurned"] >= 1000) & (sub_df1["AcresBurned"] < 5000)]
    sub_df3 = medium_df_list[(medium_df_list["StructuresDestroyed"] > 0)]
    y = medium_df_list[["StructuresDestroyed"]].values.tolist()
    ax.hist(y, stacked=True)
    plt.xlabel("Structures Destroyed")
    plt.ylabel("Frequency")
    st.pyplot(fig)
if charttype == "Histogram" and datatype == "Structures Destroyed" and selected_map == "Large (>5000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Frequency of Structures Destroyed by Fires")
    large_df_list = sub_df1[sub_df1["AcresBurned"] >= 5000]
    sub_df3 = large_df_list[(large_df_list["StructuresDestroyed"] > 0)]
    y = large_df_list[["StructuresDestroyed"]].values.tolist()
    ax.hist(y, stacked=True)
    plt.xlabel("Structures Destroyed")
    plt.ylabel("Frequency")
    st.pyplot(fig)

if charttype == "Scatterplot" and datatype == "Structures Damaged" and selected_map == "Small (<1000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Plot of Structures Damaged and Acres Burned")
    small_df_list = sub_df1[(sub_df1["AcresBurned"] > 0.1) & (sub_df1["AcresBurned"] < 1000) & (sub_df1["StructuresDamaged"] > 0)]
    x = small_df_list[["AcresBurned"]].values.tolist()
    y = small_df_list[["StructuresDamaged"]].values.tolist()
    ax.scatter(x, y, color="cyan")
    plt.xlabel("Acres Burned")
    plt.ylabel("Structures Damaged")
    st.pyplot(fig)
if charttype == "Scatterplot" and datatype == "Structures Damaged" and selected_map == "Medium (>1000 and 5000< Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Plot of Structures Damaged and Acres Burned")
    medium_df_list = sub_df1[(sub_df1["AcresBurned"] >= 1000) & (sub_df1["AcresBurned"] < 5000) & (sub_df1["StructuresDamaged"] > 0)]
    x = medium_df_list[["AcresBurned"]].values.tolist()
    y = medium_df_list[["StructuresDamaged"]].values.tolist()
    ax.scatter(x, y, color="yellow")
    plt.xlabel("Acres Burned")
    plt.ylabel("Structures Damaged")
    st.pyplot(fig)
if charttype == "Scatterplot" and datatype == "Structures Damaged" and selected_map == "Large (>5000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Plot of Structures Damaged and Acres Burned")
    large_df_list = sub_df1[sub_df1["AcresBurned"] >= 5000 & (sub_df1["StructuresDamaged"] > 0)]
    x = large_df_list[["AcresBurned"]].values.tolist()
    y = large_df_list[["StructuresDamaged"]].values.tolist()
    ax.scatter(x, y, color="green")
    plt.xlabel("Acres Burned")
    plt.ylabel("Structures Damaged")
    st.pyplot(fig)

if charttype == "Scatterplot" and datatype == "Structures Destroyed" and selected_map == "Small (<1000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Plot of Structures Destroyed and Acres Burned")
    small_df_list = sub_df1[(sub_df1["AcresBurned"] > 0.1) & (sub_df1["AcresBurned"] < 1000) & (sub_df1["StructuresDestroyed"] > 0)]
    x = small_df_list[["AcresBurned"]].values.tolist()
    y = small_df_list[["StructuresDestroyed"]].values.tolist()
    ax.scatter(x, y, color="red")
    plt.xlabel("Acres Burned")
    plt.ylabel("Structures Destroyed")
    st.pyplot(fig)
if charttype == "Scatterplot" and datatype == "Structures Destroyed" and selected_map == "Medium (>1000 and 5000< Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Plot of Structures Destroyed and Acres Burned")
    medium_df_list = sub_df1[(sub_df1["AcresBurned"] >= 1000) & (sub_df1["AcresBurned"] < 5000) & (sub_df1["StructuresDestroyed"] > 0)]
    x = medium_df_list[["AcresBurned"]].values.tolist()
    y = medium_df_list[["StructuresDestroyed"]].values.tolist()
    ax.scatter(x, y, color="orange")
    plt.xlabel("Acres Burned")
    plt.ylabel("Structures Destroyed")
    st.pyplot(fig)
if charttype == "Scatterplot" and datatype == "Structures Destroyed" and selected_map == "Large (>5000 Acres Burned)":
    fig,ax = plt.subplots()
    st.title("Plot of Structures Destroyed and Acres Burned")
    large_df_list = sub_df1[sub_df1["AcresBurned"] >= 5000 & (sub_df1["StructuresDestroyed"] > 0)]
    x = large_df_list[["AcresBurned"]].values.tolist()
    y = large_df_list[["StructuresDestroyed"]].values.tolist()
    ax.scatter(x, y, color="purple")
    plt.xlabel("Acres Burned")
    plt.ylabel("Structures Destroyed")
    st.pyplot(fig)


data_radio = st.sidebar.select_slider("Please select what piece of data you would like to see:", ["Injuries", "Responding Personnel"])
data_slider = st.sidebar.radio("What would like to see from the selected data?", ["Chart", "10 Max Map", "10 Min Map"])

if data_radio == "Injuries" and data_slider == "Chart":
        st.title("Injuries Compared to Acres Burned")
        fig,ax = plt.subplots()
        color_radio = st.sidebar.radio("Please select the color of the chart:", ["orange", "red", "blue", "green"])
        sub_df2 = sub_df1[(df_cal["AcresBurned"] > 0) & (df_cal["Injuries"] > 0)]
        x = []
        y = []
        for i in sub_df2[["Injuries"]]:
                y.append(sub_df2[["Injuries"]][i])
        for i in sub_df2[["AcresBurned"]]:
                x.append(sub_df2[["AcresBurned"]][i])
        ax.scatter(x, y, color=color_radio, marker="H", s=10)
        plt.xlabel("Acres Burned")
        plt.ylabel("Injuries")
        st.pyplot(fig)
elif data_radio == "Responding Personnel" and data_slider == "Chart":
        st.title("Responding Personnel and Acres Burned")
        color_radio = st.sidebar.radio("Please select the color of the chart:", ["orange", "red", "blue", "green"])
        fig,ax = plt.subplots()
        sub_df2 = sub_df1[(df_cal["AcresBurned"] > 0) & (df_cal["PersonnelInvolved"] > 0)]
        x = []
        y = []
        for i in sub_df2[["PersonnelInvolved"]]:
                y.append(sub_df2[["PersonnelInvolved"]][i])
        for i in sub_df2[["AcresBurned"]]:
                x.append(sub_df2[["AcresBurned"]][i])
        ax.scatter(x, y, color=color_radio, marker="*", s=10)
        plt.xlabel("Acres Burned")
        plt.ylabel("Personnel Involved")
        st.pyplot(fig)
elif data_radio == "Injuries" and data_slider == "10 Max Map":
        st.title("10 Fires With the Most Injuries")
        sub_df3 = sub_df1[(sub_df1["Injuries"] > 0)]
        sub_df4 = sub_df3.copy()
        sub_df5 = sub_df4.sort_values("Injuries", axis=0, ascending=False, inplace=True)
        sub_df6 = pd.DataFrame(sub_df4).reset_index()
        sub_df7 = sub_df6.loc[:9,]
        sub_df8 = sub_df7[["lat", "lon"]]
        st.map(sub_df8) # The above series of variables sorts the data in a step-by-step process
elif data_radio == "Responding Personnel" and data_slider == "10 Max Map":
        st.title("10 Fires With the Most Responding Personnel")
        sub_df3 = sub_df1[(sub_df1["PersonnelInvolved"] > 0)]
        sub_df4 = sub_df3.copy()
        sub_df5 = sub_df4.sort_values("PersonnelInvolved", axis=0, ascending=False, inplace=True)
        sub_df6 = pd.DataFrame(sub_df4).reset_index()
        sub_df7 = sub_df6.loc[:9,]
        sub_df8 = sub_df7[["lat", "lon"]]
        st.map(sub_df8)
elif data_radio == "Injuries" and data_slider == "10 Min Map":
        st.title("10 Fires With the Fewest Injuries")
        sub_df3 = sub_df1[(sub_df1["Injuries"] > 0)]
        sub_df4 = sub_df3.copy()
        sub_df5 = sub_df4.sort_values("Injuries", axis=0, ascending=True, inplace=True)
        sub_df6 = pd.DataFrame(sub_df4).reset_index()
        sub_df7 = sub_df6.loc[:9,]
        sub_df8 = sub_df7[["lat", "lon"]]
        st.map(sub_df8)
elif data_radio == "Responding Personnel" and data_slider == "10 Min Map":
        st.title("10 Fires With the Fewest Responding Personnel")
        sub_df3 = sub_df1[(sub_df1["PersonnelInvolved"] > 0)]
        sub_df4 = sub_df3.copy()
        sub_df5 = sub_df4.sort_values("PersonnelInvolved", axis=0, ascending=True, inplace=True)
        sub_df6 = pd.DataFrame(sub_df4).reset_index()
        sub_df7 = sub_df6.loc[:9,]
        sub_df8 = sub_df7[["lat", "lon"]]
        st.map(sub_df8)

