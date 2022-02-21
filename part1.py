import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

    
def tab1():
    st.title("Rainfall \n") 
    st.markdown('#')

    # Keys
    keys = ['a1','b1','c1','d1','e1','f1','g1','h1','i1','j1','k1','l1','m1','n1','o1','p1']


    # TABLE 1
    df1 = pd.read_csv("Data/Rainfall CHIRPS/CHIRPS_observations.csv") 

    st.markdown('### Observations')

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df1.District))
    checka1 = col1.checkbox(all_districts[0], True, key=keys[0])
    checkb1 = col1.checkbox(all_districts[1], True, key=keys[1])
    checkc1 = col1.checkbox(all_districts[2], True, key=keys[2])
    checkd1 = col1.checkbox(all_districts[3], True, key=keys[3])
    checke1 = col1.checkbox(all_districts[4], True, key=keys[4])
    checkf1 = col1.checkbox(all_districts[5], True, key=keys[5])
    
    ob_districts = [all_districts[i] for i,d in enumerate([checka1, checkb1, checkc1, checkd1, checke1, checkf1]) if d]
    if len(ob_districts) == 0:
        ob_districts = all_districts
    ob_accumulation = col1.multiselect("Accumulation", list(set(df1.Accumulation)), [], key = keys[6])
    if not ob_accumulation:
        ob_accumulation = list(set(df1.Accumulation))

    # Filtering data
    data = df1[np.logical_and(df1['Accumulation'].isin(ob_accumulation), df1['District'].isin(ob_districts))]
     
    # Displaying data   
    c = alt.Chart(data).mark_circle().encode(
        alt.X('Years', scale=alt.Scale(zero=False)),
        alt.Y('Value',  title = 'Precipitation (mm)'),
        color = 'District',
        tooltip=['Years','Accumulation','District','Value'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)



    st.markdown('### Forecasts')
    # TABLE 2
    df2 = pd.read_csv("Data/Ensemble Rainfall/ECMWF_rainfall.csv")

    col1, col, col2 = st.columns([10, 1, 30]) 
    subcol1, subcol2, subcol3 = st.columns([1,1,1])

    # Widgets
    col1.write('District')
    all_districts = list(set(df2.District))
    pb_dist = []
    checkh1 = col1.checkbox(all_districts[0], True, key=keys[7])
    checki1 = col1.checkbox(all_districts[1], True, key=keys[8])
    checkj1 = col1.checkbox(all_districts[2], True, key=keys[9])
    checkk1 = col1.checkbox(all_districts[3], True, key=keys[10])
    checkl1 = col1.checkbox(all_districts[4], True, key=keys[11])
    checkm1 = col1.checkbox(all_districts[5], True, key=keys[12])
    
    pb_districts = [all_districts[i] for i,d in enumerate([checkh1, checki1, checkj1, checkk1,checkl1,checkm1]) if d]
    if len(pb_districts) == 0:
        pb_districts = all_districts
    pb_accumulation = subcol1.multiselect("Acumulation", list(set(df2.Acumulation)), [], key = keys[13])
    if not pb_accumulation:
        pb_accumulation = list(set(df2.Acumulation))
    pb_ensemble = subcol2.multiselect("Ensemble Member", list(set(df2.Ensemble_number)), [], key = keys[14])
    if not pb_ensemble:
        pb_ensemble = list(set(df2.Ensemble_number))
    pb_month = subcol3.multiselect("Month of forecast issue", list(set(df2.Forecast_month)), [], key = keys[15])
    if not pb_month:
        pb_month = list(set(df2.Forecast_month))    

    # Filtering data
    data = df2[np.logical_and(df2['Acumulation'].isin(pb_accumulation), df2['District'].isin(pb_districts))]
    data = data[np.logical_and(data['Ensemble_number'].isin(pb_ensemble), data['Forecast_month'].isin(pb_month))]

     
    # Displaying data   
    c = alt.Chart(data).mark_circle().encode(
        alt.X('Year', title = 'Years', scale=alt.Scale(zero=False)),
        alt.Y('Value',  title = 'Precipitation (mm)'),
        color = 'District',
        tooltip=['Year','Ensemble_number', 'Acumulation', 'Value', 'District', 'Forecast_month'])
    line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule().encode(y='y')
    layers = alt.layer(line, c).configure_area(tooltip = True).interactive()

    col2.altair_chart(layers, use_container_width=True)
     
