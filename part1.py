import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

import SessionState

    
def main(ss):
    st.title("Rainfall \n") 
    st.markdown('#')

    # Keys
    keys = ['a1','b1','c1','d1','e1','f1','g1','h1','i1','j1','k1','l1']

    def implementation(i):
        if i == 0:
            ss.a1 = st.session_state.a1
        elif i == 1:
            ss.b1 = st.session_state.b1
        elif i == 2:
            ss.c1 = st.session_state.c1
        elif i == 3:
            ss.d1 = st.session_state.d1
        elif i == 4:
            ss.e1 = st.session_state.e1
        elif i == 5:
            ss.f1 = st.session_state.f1
        elif i == 6:
            ss.g1 = st.session_state.g1
        elif i == 7:
            ss.h1 = st.session_state.h1
        elif i == 8:
            ss.i1 = st.session_state.i1
        elif i == 9:
            ss.j1 = st.session_state.j1
        elif i == 10:
            ss.k1 = st.session_state.k1
        elif i == 11:
            ss.l1 = st.session_state.l1


    # TABLE 1
    df1 = pd.read_csv("Data/Rainfall CHIRPS/CHIRPS_observations.csv") 

    st.markdown('### Observations')

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df1.District))
    checka1 = col1.checkbox(all_districts[0], ss.a1, key=keys[0], on_change = implementation, args = [0])
    checkb1 = col1.checkbox(all_districts[1], ss.b1, key=keys[1], on_change = implementation, args = [1])
    checkc1 = col1.checkbox(all_districts[2], ss.c1, key=keys[2], on_change = implementation, args = [2])
    checkd1 = col1.checkbox(all_districts[3], ss.d1, key=keys[3], on_change = implementation, args = [3])
    ob_districts = [all_districts[i] for i,d in enumerate([checka1, checkb1, checkc1, checkd1]) if d]
    if len(ob_districts) == 0:
        ob_districts = all_districts
    ob_accumulation = col1.multiselect("Accumulation", list(set(df1.Accumulation)), ss.e1, key = keys[4], on_change = implementation, args = [4])
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
    checkf1 = col1.checkbox(all_districts[0], ss.f1, key=keys[5], on_change = implementation, args = [5])
    checkg1 = col1.checkbox(all_districts[1], ss.g1, key=keys[6], on_change = implementation, args = [6])
    checkh1 = col1.checkbox(all_districts[2], ss.h1, key=keys[7], on_change = implementation, args = [7])
    checki1 = col1.checkbox(all_districts[3], ss.i1, key=keys[8], on_change = implementation, args = [8])
    pb_districts = [all_districts[i] for i,d in enumerate([checkf1, checkg1, checkh1, checki1]) if d]
    if len(pb_districts) == 0:
        pb_districts = all_districts
    pb_accumulation = subcol1.multiselect("Acumulation", list(set(df2.Acumulation)), ss.j1, key = keys[9], on_change = implementation, args = [9])
    if not pb_accumulation:
        pb_accumulation = list(set(df2.Acumulation))
    pb_ensemble = subcol2.multiselect("Ensemble Member", list(set(df2.Ensemble_number)), ss.k1, key = keys[10], on_change = implementation, args = [10])
    if not pb_ensemble:
        pb_ensemble = list(set(df2.Ensemble_number))
    pb_month = subcol3.multiselect("Month of forecast issue", list(set(df2.Forecast_month)), ss.l1, key = keys[11], on_change = implementation, args = [11])
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
     
