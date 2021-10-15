import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

    
def main():
    st.title("Rainfall \n") 
    st.markdown('#')

    # TABLE 1
    df = pd.read_csv("Data/Rainfall CHIRPS/CHIRPS_observations.csv") 

    st.markdown('### Observations')

    col1, col, col2 = st.columns([10, 1, 30]) 

    # Widgets
    col1.write('District')
    all_districts = list(set(df.District))
    ob_dist = []
    for i,d in enumerate(all_districts):
        a = col1.checkbox(d, True, key=i)
        ob_dist.append(a)
    districts = [all_districts[i] for i,d in enumerate(ob_dist) if d]
    if len(districts) == 0:
        districts = all_districts
    ob_accumulation = col1.multiselect("Accumulation", list(set(df.Accumulation)), [], key = 'ob_ac')
    if not ob_accumulation:
        ob_accumulation = list(set(df.Accumulation))

    # Filtering data
    data = df[np.logical_and(df['Accumulation'].isin(ob_accumulation), df['District'].isin(districts))]
     
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

    df = pd.read_csv("Data/Ensemble Rainfall/ECMWF_rainfall.csv")

    col1, col, col2 = st.columns([10, 1, 30]) 
    subcol1, subcol2, subcol3 = st.columns([1,1,1])

    # Widgets
    col1.write('District')
    all_districts = list(set(df.District))
    pb_dist = []
    for d in all_districts:
        b = col1.checkbox(d, True)
        pb_dist.append(b)
    districts = [all_districts[i] for i,d in enumerate(pb_dist) if d]
    if len(districts) == 0:
        districts = all_districts
    pb_accumulation = subcol1.multiselect("Acumulation", list(set(df.Acumulation)), [], key = 'pb_ac')
    if not pb_accumulation:
        pb_accumulation = list(set(df.Acumulation))
    pb_ensemble = subcol2.multiselect("Ensemble Member", list(set(df.Ensemble_number)), [], key = 'pb_en')
    if not pb_ensemble:
        pb_ensemble = list(set(df.Ensemble_number))
    pb_month = subcol3.multiselect("Month of forecast issue", list(set(df.Forecast_month)), [], key = 'pb_mo')
    if not pb_month:
        pb_month = list(set(df.Forecast_month))    

    # Filtering data
    data = df[np.logical_and(df['Acumulation'].isin(pb_accumulation), df['District'].isin(districts))]
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
     
